\set ON_ERROR_STOP on
\getenv app_password POSTGRES_APP_PASSWORD
BEGIN;
SELECT 'CREATE ROLE oak_app LOGIN' WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'oak_app') \gexec
SELECT format('ALTER ROLE oak_app PASSWORD %L', :'app_password') \gexec
CREATE TABLE IF NOT EXISTS embedding_config (
    singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
    model text NOT NULL,
    dimensions integer NOT NULL CHECK (dimensions = 768)
);
INSERT INTO embedding_config (model, dimensions)
VALUES ('text-embedding-nomic-embed-text-v1.5', 768) ON CONFLICT DO NOTHING;
CREATE TABLE IF NOT EXISTS documents (
    id text PRIMARY KEY,
    document_id text NOT NULL,
    source text NOT NULL,
    source_type text NOT NULL,
    title text NOT NULL,
    object_key text NOT NULL,
    status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'approved', 'superseded')),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source, document_id)
);
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id text PRIMARY KEY,
    entry_id text NOT NULL REFERENCES documents(id),
    text text NOT NULL,
    metadata jsonb NOT NULL,
    embedding vector(768) NOT NULL
);
CREATE INDEX IF NOT EXISTS chunks_entry_id_idx ON chunks(entry_id);
GRANT CONNECT ON DATABASE oak_fabric TO oak_app;
GRANT USAGE ON SCHEMA public TO oak_app;
GRANT SELECT ON embedding_config TO oak_app;
GRANT SELECT, INSERT ON documents, chunks TO oak_app;
GRANT UPDATE(status) ON documents TO oak_app;
COMMIT;
