import json
import math
import urllib.error
import urllib.request


class ModelError(RuntimeError):
    """The model service failed or returned an invalid result."""


class ModelClient:
    def __init__(self, base_url: str, embedding_model: str, generation_model: str):
        self.base_url = base_url.rstrip("/")
        self.embedding_model = embedding_model
        self.generation_model = generation_model

    def _post(self, path: str, payload: dict) -> dict:
        request = urllib.request.Request(
            self.base_url + path, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise ModelError("Model request failed; check LM Studio availability and model configuration") from exc

    def embed(self, texts: list[str], *, query: bool = False) -> list[list[float]]:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("Embedding inputs must be nonempty")
        prefix = "search_query: " if query else "search_document: "
        result = self._post("/embeddings", {"model": self.embedding_model, "input": [prefix + t for t in texts]})
        try:
            if result.get("model") != self.embedding_model:
                raise ValueError("Model mismatch")
            entries = sorted(result["data"], key=lambda entry: entry["index"])
            if [entry["index"] for entry in entries] != list(range(len(texts))):
                raise ValueError("Embedding count or index mismatch")
            vectors = [entry["embedding"] for entry in entries]
            for vector in vectors:
                if len(vector) != 768 or any(type(x) not in (int, float) or not math.isfinite(x) for x in vector):
                    raise ValueError("Expected 768 finite dimensions")
                if sum(x * x for x in vector) == 0:
                    raise ValueError("Zero embedding")
            return vectors
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            raise ModelError("Invalid embedding response; index requires the configured 768-dimensional model") from exc
