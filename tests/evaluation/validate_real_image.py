"""Check a saved real-image draft against visually transcribed panel 11 facts."""
import argparse
import hashlib
import json
from pathlib import Path

from src.extraction.architecture import ArchitectureObservation


def validate(path: Path) -> dict:
    draft = json.loads(path.read_text())
    expected = json.loads(Path('tests/evaluation/ai-embeddings-expected.json').read_text())
    analysis = ArchitectureObservation.model_validate(draft['analysis'])
    labels = {c.id: ' '.join(c.label.casefold().split()) for c in analysis.components}
    expected_labels = {label.casefold() for label in expected['components']}
    edges = {(labels[e.source], labels[e.target]) for e in analysis.connections}
    expected_edges = {(a.casefold(), b.casefold()) for a, b in expected['connections']}
    missing_nodes = sorted(expected_labels - set(labels.values()))
    missing_edges = sorted(expected_edges - edges)
    unexpected_panel_edges = sorted((a, b) for a, b in edges if a in expected_labels and b in expected_labels and (a, b) not in expected_edges)
    source = Path(draft['source']).read_bytes()
    preserved = Path(draft['preserved_source']).read_bytes()
    intact = source == preserved and hashlib.sha256(source).hexdigest() == draft['image']['sha256']
    passed = intact and not missing_nodes and not missing_edges and not unexpected_panel_edges
    return {'draft': str(path), 'model': draft['model'], 'scope': expected['scope'],
            'result': 'PASS' if passed else 'FAIL', 'source_bytes_preserved': intact,
            'missing_nodes': missing_nodes, 'missing_edges': missing_edges,
            'unexpected_panel_edges': unexpected_panel_edges,
            'limitation': 'Exact panel-11 subset check; full visual review and human approval are separate.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('draft', type=Path)
    args = parser.parse_args()
    result = validate(args.draft)
    print(json.dumps(result, indent=2))
    raise SystemExit(result['result'] != 'PASS')
