"""Real LM Studio smoke test with a labeled synthetic diagram."""
import json
import tempfile
from pathlib import Path

from src.embeddings.client import ModelClient
from src.ingestion.images import process_image

source=Path('tests/fixtures/synthetic-architecture.png')
model=ModelClient('http://localhost:1234/v1','text-embedding-nomic-embed-text-v1.5','google/gemma-4-e4b')
with tempfile.TemporaryDirectory(prefix='oak-image-smoke-') as folder:
    artifact=process_image(source,model,Path(folder))
    draft=json.loads(artifact.read_text())
    Path('logs/validation/phase-3.1-synthetic-analysis.json').write_text(json.dumps(draft,indent=2)+'\n')
    assert (Path(folder)/draft['preserved_source']).read_bytes()==source.read_bytes()
    analysis=draft['analysis']
    labels={c['id']:c['label'].casefold() for c in analysis['components']}
    assert set(labels.values())=={'client','api'}, labels
    assert len(analysis['connections'])==1, analysis['connections']
    edge=analysis['connections'][0]
    assert (labels[edge['source']],labels[edge['target']])==('client','api'), edge
    assert all(c['technology'] is None for c in analysis['components']), analysis['components']
    print(json.dumps({'result':'PASS','fixture':'synthetic only','components':['Client','API'],'direction':'Client -> API','source_bytes_preserved':True,'real_architecture_acceptance':'pending'}))
