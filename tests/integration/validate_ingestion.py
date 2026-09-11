"""Run through stdin inside the API container after bootstrap."""
import hashlib
import json
import os
import urllib.request

from src.common.storage import database, objects

from pathlib import Path

content = Path('/tmp/oak-evaluation/storage-guide.md').read_bytes()
headers = {'Authorization': 'Bearer ' + os.environ['FABRIC_API_KEY'], 'Content-Type': 'text/markdown'}
def request(path, data=None):
    req = urllib.request.Request('http://localhost:8000' + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=300) as response:
        return json.load(response)
first = request('/ingest/document?source=tests/fixtures/storage-guide.md', content)
second = request('/ingest/document?source=tests/fixtures/storage-guide.md', content)
assert first['id'] == second['id'] and not second['created']
assert first['document_id'] == hashlib.sha256(content).hexdigest()
review = request('/documents/' + first['id'])
assert len(review['chunks']) == first['chunks']
assert all(c['metadata']['source'] == 'tests/fixtures/storage-guide.md' for c in review['chunks'])
with database() as conn:
    dimensions = conn.execute('SELECT DISTINCT vector_dims(embedding) FROM chunks WHERE entry_id=%s', (first['id'],)).fetchall()
    assert dimensions == [(768,)]
    assert conn.execute('SELECT count(*) FROM documents WHERE id=%s', (first['id'],)).fetchone()[0] == 1
    privileges = conn.execute("SELECT rolsuper, rolcreatedb, rolcreaterole FROM pg_roles WHERE rolname=current_user").fetchone()
    assert privileges == (False, False, False)
obj = objects().get_object('oak-sources', review['object_key'])
try:
    assert obj.read() == content
finally:
    obj.close(); obj.release_conn()
print(json.dumps({'result':'PASS','entry_id':first['id'],'chunks':first['chunks'],'dimensions':768,'deduplicated':True,'source_bytes_preserved':True,'restricted_db_role':True,'status':first['status']}))
