"""Check real Compose storage; run write, restart services, then read."""
import argparse
import os
import subprocess
import uuid


COMPOSE = ["docker", "compose"]
if os.getenv("DOCKER_CONFIG"):
    COMPOSE = ["docker", "--config", os.environ["DOCKER_CONFIG"], "compose"]


def run(service: str, command: list[str], data: str | None = None) -> str:
    result = subprocess.run(
        [*COMPOSE, "exec", "-T", service, *command], input=data,
        text=True, capture_output=True, timeout=30, check=True,
    )
    return result.stdout.strip()


def validate(mode: str, token: str) -> None:
    # UUID validation prevents SQL/shell injection from the command line.
    token = str(uuid.UUID(token))
    if mode == "write":
        run("postgres", ["psql", "-U", "oak", "-d", "oak_fabric", "-v", "ON_ERROR_STOP=1"], f"""
CREATE TABLE IF NOT EXISTS foundation_probe (id uuid PRIMARY KEY, embedding vector(3));
INSERT INTO foundation_probe VALUES ('{token}', '[1,2,3]') ON CONFLICT DO NOTHING;
""")
        run("minio", ["sh", "-ec", '''
curl --fail --silent --show-error --aws-sigv4 'aws:amz:us-east-1:s3' --user "$MINIO_ROOT_USER:$MINIO_ROOT_PASSWORD" -X PUT http://localhost:9000/oak-foundation-check
curl --fail --silent --show-error --aws-sigv4 'aws:amz:us-east-1:s3' --user "$MINIO_ROOT_USER:$MINIO_ROOT_PASSWORD" -X PUT --data-binary "$1" "http://localhost:9000/oak-foundation-check/$1"
''', "probe", token])
    distance = run("postgres", ["psql", "-U", "oak", "-d", "oak_fabric", "-At", "-v", "ON_ERROR_STOP=1", "-c",
        f"SELECT embedding <-> '[1,2,3]'::vector FROM foundation_probe WHERE id = '{token}';"])
    assert distance == "0", f"Vector round-trip failed: {distance!r}"
    body = run("minio", ["sh", "-ec", '''
curl --fail --silent --show-error --aws-sigv4 'aws:amz:us-east-1:s3' --user "$MINIO_ROOT_USER:$MINIO_ROOT_PASSWORD" "http://localhost:9000/oak-foundation-check/$1"
''', "probe", token])
    assert body == token, "Object round-trip failed"
    print(f"PASS: {mode} PostgreSQL vector and MinIO object round-trips for {token}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["write", "read"])
    parser.add_argument("token", help="UUID shared between write and post-restart read")
    args = parser.parse_args()
    validate(args.mode, args.token)
