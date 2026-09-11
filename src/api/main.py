from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from src.common.config import Settings


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

    return app
