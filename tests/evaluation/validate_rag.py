"""Run inside the API container with fixtures copied to /tmp/oak-evaluation."""
import json
import os
import urllib.request
from pathlib import Path

from src.common.storage import database

headers = {'Authorization': 'Bearer ' + os.environ['FABRIC_API_KEY'], 'Content-Type':'application/json'}
def call(path, payload):
    req = urllib.request.Request('http://localhost:8000'+path, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=300) as response:
        return json.load(response)

with database() as conn:
    entry_id, status = conn.execute("SELECT id, status FROM documents WHERE source=%s ORDER BY created_at DESC LIMIT 1", ('tests/fixtures/storage-guide.md',)).fetchone()
if status == 'draft':
    before = call('/search', {'question':'Where are original documents stored?'})
    assert all(r['entry_id'] != entry_id for r in before['results']), 'Draft leaked into retrieval'
    print(json.dumps({'check':'draft_exclusion', 'result':'PASS'}), flush=True)
call('/documents/'+entry_id+'/approve', {})
for case in json.loads(Path('/tmp/oak-evaluation/rag-cases.json').read_text()):
    result = call('/rag/query', {'question':case['question']})
    assert result['abstained'] == case['abstain'], result
    if not case['abstain']:
        assert all(phrase in result['answer'] for phrase in case['expected_phrases']), result
        assert result['citations'], result
        for citation in result['citations']:
            assert citation['source'] == case['expected_source']
            with database() as conn:
                text = conn.execute('SELECT text FROM chunks WHERE chunk_id=%s', (citation['chunk_id'],)).fetchone()[0]
            assert citation['quote'] in text
    print(json.dumps({'question':case['question'],'result':'PASS','response':result}), flush=True)
