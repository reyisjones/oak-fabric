"""Analyze a local image into a preserved source and reviewable JSON draft."""
import argparse
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.embeddings.client import ModelClient
from src.extraction.images import MAX_IMAGE_BYTES, analyze_image, inspect_image


ROOT = Path(__file__).resolve().parents[2]


def process_image(source: Path, model: ModelClient, root: Path = ROOT, *, focus: str | None = None) -> Path:
    # Bound reads as well as decoder input; never load an arbitrarily large file.
    with source.open("rb") as stream:
        content = stream.read(MAX_IMAGE_BYTES + 1)
    info = inspect_image(content)
    originals = root / "images" / "processed"
    originals.mkdir(parents=True, exist_ok=True)
    original = originals / f"{info.sha256}.{info.extension}"
    try:
        with original.open("xb") as stream:
            stream.write(content)
    except FileExistsError:
        if original.read_bytes() != content:
            raise ValueError("Preserved source differs from its checksum; inspect before retrying")
    observation = analyze_image(content, model, focus=focus)
    drafts = root / "documents" / "generated" / "image-analysis"
    drafts.mkdir(parents=True, exist_ok=True)
    output = drafts / f"{info.sha256}-{uuid4().hex}.json"
    payload = {
        "schema_version": 1, "status": "review", "created_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source), "preserved_source": original.relative_to(root).as_posix(),
        "focus": focus, "image": asdict(info), "model": model.generation_model,
        "analysis": observation.model_dump(),
        "validation": {"structure": "passed", "visual_accuracy": "not_reviewed"},
    }
    # Each run creates a new artifact; user corrections and earlier drafts are never overwritten.
    with output.open("x") as stream:
        json.dump(payload, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--model", default=os.getenv("VISION_MODEL", "google/gemma-4-e4b"))
    parser.add_argument("--base-url", default=os.getenv("MODEL_BASE_URL", "http://localhost:1234/v1"))
    parser.add_argument("--focus", help="Limit analysis to a named panel; original image is preserved in full")
    args = parser.parse_args()
    client = ModelClient(args.base_url, "text-embedding-nomic-embed-text-v1.5", args.model)
    print(process_image(args.source, client, focus=args.focus))
