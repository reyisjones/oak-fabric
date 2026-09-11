import hmac
import logging
import os
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
import psycopg
from minio.error import MinioException
from urllib3.exceptions import HTTPError as StorageHTTPError
from pydantic import BaseModel, Field

from src.common.config import Settings
from src.common.storage import database
from src.embeddings.client import ModelClient, ModelError
from src.extraction.documents import ExtractionError, MAX_DOCUMENT_BYTES
from src.ingestion.documents import approve, ingest
from src.retrieval.search import search
from src.rag.answer import query


def authorize(authorization: str | None = Header(default=None)) -> None:
    key = os.getenv("FABRIC_API_KEY", "")
    if not key:
        raise HTTPException(503, "FABRIC_API_KEY is not configured")
    if not authorization or not hmac.compare_digest(authorization.encode(), ("Bearer " + key).encode()):
        raise HTTPException(401, "Valid bearer token required")


def model_client() -> ModelClient:
    return ModelClient(
        os.getenv("MODEL_BASE_URL", "http://localhost:1234/v1"),
        os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5"),
        os.getenv("GENERATION_MODEL", "google/gemma-4-e4b"),
    )


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=2000, pattern=r"\S")
    top_k: int = Field(default=5, ge=1, le=5)


class Health(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "oak-fabric"


def create_app() -> FastAPI:
    settings = Settings.from_env()
    app = FastAPI(
        title="Open Architecture Knowledge Fabric",
        version="0.1.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.environment != "production" else None,
    )

    @app.get("/health", response_model=Health)
    def health() -> Health:
        """Process liveness only; storage readiness is checked separately."""
        return Health()

    @app.exception_handler(ModelError)
    async def model_error(request: Request, exc: ModelError) -> JSONResponse:
        return failure("model", 502)

    def failure(component: str, status: int = 503) -> JSONResponse:
        request_id = str(uuid4())
        logging.getLogger("uvicorn.error").error("operation_failed component=%s request_id=%s", component, request_id)
        return JSONResponse(status_code=status, content={"detail": f"{component} unavailable", "request_id": request_id})

    async def storage_error(request: Request, exc: Exception) -> JSONResponse:
        return failure("storage")

    for error in (psycopg.Error, MinioException, StorageHTTPError):
        app.add_exception_handler(error, storage_error)

    @app.post("/ingest/document", dependencies=[Depends(authorize)])
    async def ingest_document(request: Request, source: str = Query(min_length=1, max_length=500)) -> dict:
        content = bytearray()
        async for data in request.stream():
            if len(content) + len(data) > MAX_DOCUMENT_BYTES:
                raise HTTPException(413, "Document exceeds 20 MiB")
            content.extend(data)
        try:
            return await run_in_threadpool(ingest, source, bytes(content), model_client())
        except (ExtractionError, ValueError) as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get("/documents/{entry_id}", dependencies=[Depends(authorize)])
    def review_document(entry_id: str) -> dict:
        with database() as conn:
            record = conn.execute("SELECT source, title, status, document_id, object_key FROM documents WHERE id = %s", (entry_id,)).fetchone()
            if record is None:
                raise HTTPException(404, "Document not found")
            chunks = conn.execute("SELECT text, metadata FROM chunks WHERE entry_id = %s ORDER BY chunk_id", (entry_id,)).fetchall()
        return dict(zip(["source", "title", "status", "document_id", "object_key"], record)) | {"chunks": [{"text": c[0], "metadata": c[1]} for c in chunks]}

    @app.post("/documents/{entry_id}/approve", dependencies=[Depends(authorize)])
    def approve_document(entry_id: str) -> dict:
        if not approve(entry_id):
            raise HTTPException(404, "Document not found")
        return {"id": entry_id, "status": "approved"}

    @app.post("/search", dependencies=[Depends(authorize)])
    def search_documents(payload: Question) -> dict:
        return {"results": search(payload.question, model_client(), payload.top_k)}

    @app.post("/rag/query", dependencies=[Depends(authorize)])
    def rag_query(payload: Question) -> dict:
        return query(payload.question, model_client(), payload.top_k)

    return app
