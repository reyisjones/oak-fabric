"""Intentional faults against real storage: no partial metadata publication."""
import json
import uuid

import psycopg
from src.common.storage import database
from src.embeddings.client import ModelClient, ModelError
from src.ingestion.documents import ingest


class FailedModel(ModelClient):
    def embed(self, texts, *, query=False):
        raise ModelError('Intentional model outage')


class InvalidVectorModel(ModelClient):
    def embed(self, texts, *, query=False):
        return [[1.0] * 767 for text in texts]


for model_type, expected in [(FailedModel, ModelError), (InvalidVectorModel, psycopg.DataError)]:
    source = 'tests/faults/' + str(uuid.uuid4()) + '.md'
    model = model_type('http://unused', 'text-embedding-nomic-embed-text-v1.5', 'google/gemma-4-e4b')
    try:
        ingest(source, b'# Fault injection\nThis is a controlled rollback test.', model)
    except expected:
        pass
    else:
        raise AssertionError('Injected failure was not detected')
    with database() as conn:
        assert conn.execute('SELECT count(*) FROM documents WHERE source=%s', (source,)).fetchone()[0] == 0
    print(json.dumps({'check':model_type.__name__, 'result':'PASS', 'partial_document_rows':0}))
