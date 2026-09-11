"""Apply the explicit schema migration and least-privilege MinIO policy."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
subprocess.run(
    ['docker', 'compose', 'exec', '-T', 'postgres', 'psql', '-U', 'oak', '-d', 'oak_fabric'],
    input=(root / 'infrastructure/docker/002-documents.sql').read_text(), text=True, check=True,
)
subprocess.run(
    ['docker', 'compose', 'exec', '-T', 'minio', 'sh', '-ec', '''
export MC_CONFIG_DIR=/tmp/oak-bootstrap-mc
mc alias set oak http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null
mc mb --ignore-existing oak/oak-sources
mc admin user add oak oak-app "$MINIO_APP_PASSWORD" >/dev/null
mc admin policy create oak oak-app-policy /dev/stdin
mc admin policy attach oak oak-app-policy --user oak-app
'''], input=(root / 'infrastructure/docker/minio-app-policy.json').read_text(), text=True, check=True,
)
print('PASS: schema migration and restricted storage accounts applied')
