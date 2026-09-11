import io
import os

import psycopg
from minio import Minio
from urllib3 import PoolManager, Timeout


def database() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "postgres"), dbname="oak_fabric",
        user="oak_app", password=os.environ["DB_PASSWORD"], connect_timeout=5,
        options="-c statement_timeout=30000 -c lock_timeout=5000",
    )


def objects() -> Minio:
    return Minio(
        os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.environ["MINIO_ACCESS_KEY"], secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False, http_client=PoolManager(timeout=Timeout(connect=5, read=30), retries=False),
    )


def preserve_source(document_id: str, content: bytes) -> str:
    key = f"documents/{document_id}"
    objects().put_object("oak-sources", key, io.BytesIO(content), len(content), content_type="application/octet-stream")
    return key
