import pytest

from src.embeddings.client import ModelClient, ModelError


def client_with(monkeypatch, result):
    client = ModelClient('http://localhost:1234/v1', 'nomic', 'gemma')
    monkeypatch.setattr(client, '_post', lambda path, payload: result)
    return client


def test_orders_vectors_and_preserves_query_prefix(monkeypatch):
    client = ModelClient('http://localhost:1234/v1', 'nomic', 'gemma')
    payloads = []
    def respond(path, payload):
        payloads.append(payload)
        return {'model': 'nomic', 'data': [{'index': 1, 'embedding': [2.0] * 768}, {'index': 0, 'embedding': [1.0] * 768}]}
    monkeypatch.setattr(client, '_post', respond)
    assert client.embed(['one', 'two'], query=True)[0][0] == 1.0
    assert payloads[0]['input'] == ['search_query: one', 'search_query: two']


@pytest.mark.parametrize('vector', [[1.0]*3, [float('nan')]*768, [float('inf')]*768, [0.0]*768, [True]*768])
def test_rejects_invalid_vector(monkeypatch, vector):
    client = client_with(monkeypatch, {'model': 'nomic', 'data': [{'index': 0, 'embedding': vector}]})
    with pytest.raises(ModelError): client.embed(['text'])


@pytest.mark.parametrize('response', [None, [], 42, {}, {'model': 'wrong', 'data': []}, {'model': 'nomic', 'data': []}, {'model': 'nomic', 'data': [{'index': 1, 'embedding': [1.0]*768}]}])
def test_rejects_invalid_response(monkeypatch, response):
    with pytest.raises(ModelError): client_with(monkeypatch, response).embed(['text'])


def test_rejects_empty_input():
    client = ModelClient('http://localhost:1234/v1', 'nomic', 'gemma')
    with pytest.raises(ValueError): client.embed([' '])
