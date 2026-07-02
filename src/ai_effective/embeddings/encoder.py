from __future__ import annotations

from functools import lru_cache

import numpy as np

_DEFAULT_MODEL = "all-MiniLM-L6-v2"


class LocalEncoder:
    """Wraps a sentence-transformers model for local embedding.

    Downloads ~80 MB on first use; all inference runs on CPU — zero API calls.
    """

    def __init__(self, model_name: str = _DEFAULT_MODEL) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required. Install it with: pip install sentence-transformers"
            ) from exc

        self._model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dim: int = self._model.get_sentence_embedding_dimension()

    def encode(self, text: str) -> np.ndarray:
        return self._model.encode(
            text, normalize_embeddings=True, show_progress_bar=False
        )

    def encode_batch(self, texts: list[str]) -> np.ndarray:
        return self._model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False
        )


@lru_cache(maxsize=1)
def get_encoder(model_name: str = _DEFAULT_MODEL) -> LocalEncoder:
    """Return a cached encoder (loads model once per process)."""
    return LocalEncoder(model_name)
