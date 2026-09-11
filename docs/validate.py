"""Validate initial planning artifacts; does not validate application behavior."""
from pathlib import Path
from datetime import datetime, timezone
import re

ROOT = Path(__file__).resolve().parents[1]
required = [
    'README.md', 'docs/assessment.md', 'docs/image-inventory.md',
    'docs/architecture/vision.md', 'docs/architecture/component-map.md',
    'docs/ROADMAP.md', 'docs/learning/progress.md', 'docs/STATUS.md',
    'docs/decisions/ADR-001-incremental-foundation.md',
    'logs/issues/ISSUES.md', 'logs/runtime/docker-preflight.txt',
]
errors: list[str] = []
for name in required:
    path = ROOT / name
    if not path.is_file() or not path.read_text().strip():
        errors.append(f'Missing or empty artifact: {name}')

paths = [ROOT / 'README.md', *sorted((ROOT / 'docs').rglob('*.md')),
         *sorted((ROOT / 'logs').rglob('*.md'))]
link_count = 0
for path in paths:
    text = path.read_text()
    if text.count('```') % 2:
        errors.append(f'Unclosed code fence: {path.relative_to(ROOT)}')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        if '://' in target or target.startswith('#'):
            continue
        link_count += 1
        if not (path.parent / target.split('#')[0]).resolve().exists():
            errors.append(f'Broken link: {path.relative_to(ROOT)} -> {target}')

status = (ROOT / 'docs/STATUS.md').read_text()
for field in ['Current Phase', 'Last Completed Task', 'Current Task',
              'Pending Tasks', 'Open Issues', 'Recent Fixes',
              'Architecture Decisions', 'Next Recommended Action',
              'Completed', 'In Progress', 'Pending', 'Blocked',
              'Issues Found', 'Fixes Applied', 'Technical Decisions', 'Next Task']:
    if field not in status:
        errors.append(f'Missing status field: {field}')
issues = (ROOT / 'logs/issues/ISSUES.md').read_text()
for field in ['ID', 'Date', 'Component', 'Symptom', 'Root Cause', 'Fix', 'Validation', 'Status']:
    if f'- {field}:' not in issues:
        errors.append(f'Missing issue field: {field}')
for category in ['build', 'runtime', 'validation', 'issues']:
    if not (ROOT / 'logs' / category).is_dir():
        errors.append(f'Missing log directory: {category}')

result = '\n'.join([
    f'Documentation validation — {datetime.now(timezone.utc).date().isoformat()}',
    'Command: python3 docs/validate.py',
    f'Checked {len(required)} required artifacts, {len(paths)} Markdown documents, {link_count} local links.',
    'Checked tracking fields, issue fields, log directories, and balanced code fences.',
    'Mermaid diagram manually inspected for declared nodes and consistent relationships; no Mermaid renderer executed.',
    'Scope excludes application tests, container startup, LLM evaluation, and user learning/approval.',
    *errors,
    'Result: FAIL' if errors else 'Result: PASS',
]) + '\n'
(ROOT / 'logs/validation/initial-review.txt').write_text(result)
print(result, end='')
raise SystemExit(bool(errors))
