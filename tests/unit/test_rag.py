import json
import pytest

from src.embeddings.client import ModelClient, ModelError
from src.rag.answer import build_answer

CHUNK = {'chunk_id': 'chunk', 'entry_id': 'entry', 'text': 'MinIO preserves original source bytes.',
         'metadata': {'source': 'guide.md', 'page': None, 'section': 'Storage'}, 'score': 0.9}


def model(monkeypatch, evidence, finish='stop'):
    client = ModelClient('http://localhost:1234/v1', 'nomic', 'gemma')
    monkeypatch.setattr(client, '_post', lambda path, payload: {'model':'gemma', 'choices':[{'finish_reason':finish, 'message':{'content':json.dumps({'evidence':evidence})}}]})
    return client


def test_exact_citation_retains_provenance(monkeypatch):
    result = build_answer('Where are originals?', [CHUNK], model(monkeypatch, [{'citation':1, 'quote':CHUNK['text']}]))
    assert result['answer'] == CHUNK['text'] + ' [1]'
    assert result['citations'][0]['source'] == 'guide.md'
    assert not result['abstained']


@pytest.mark.parametrize('entry', [
    {'citation':2,'quote':'MinIO'}, {'citation':True,'quote':'MinIO'},
    {'citation':1,'quote':'S3 stores originals.'}, {'citation':1,'quote':''},
])
def test_rejects_fabricated_evidence(monkeypatch, entry):
    with pytest.raises(ModelError): build_answer('Where?', [CHUNK], model(monkeypatch, [entry]))


def test_empty_context_does_not_call_model(monkeypatch):
    client = model(monkeypatch, [])
    monkeypatch.setattr(client, '_post', lambda *args: pytest.fail('No model call expected'))
    assert build_answer('Unknown?', [], client)['abstained']


def test_model_can_abstain_with_retrieved_context(monkeypatch):
    assert build_answer('Unknown?', [CHUNK], model(monkeypatch, []))['abstained']


def test_truncated_generation_is_rejected(monkeypatch):
    with pytest.raises(ModelError): build_answer('Where?', [CHUNK], model(monkeypatch, [], 'length'))


def test_preserves_surrounding_facts_in_selected_passage(monkeypatch):
    chunk = CHUNK | {'text': 'PostgreSQL stores metadata. pgvector stores embeddings.'}
    result = build_answer('Which database and extension?', [chunk], model(monkeypatch, [{'citation':1, 'quote':'PostgreSQL stores metadata.'}]))
    assert 'pgvector stores embeddings.' in result['answer']
    assert result['citations'][0]['quote'] == chunk['text']
