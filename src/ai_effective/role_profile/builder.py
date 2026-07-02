"""RoleProfile dataclass and RoleProfileBuilder.

Building a profile is purely local:
  1. Tokenise + extract keywords  (extractor.py)
  2. Detect role domain           (extractor.py → taxonomy.py)
  3. Embed the job description    (LocalEncoder — sentence-transformers, CPU-only)
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

import numpy as np

from ai_effective.embeddings.encoder import LocalEncoder, get_encoder
from ai_effective.role_profile.extractor import detect_domain, extract_top_keywords


@dataclass
class RoleProfile:
    id: str
    title: str
    domain: str
    keywords: list[str]
    embedding: list[float]       # numpy array serialised as list for JSON
    job_description: str
    created_at: str              # ISO-8601 UTC

    # ------------------------------------------------------------------ helpers

    def embedding_array(self) -> np.ndarray:
        return np.array(self.embedding, dtype=np.float32)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> RoleProfile:
        return cls(**data)


class RoleProfileBuilder:
    """Build a RoleProfile from a plain-text job description.

    Parameters
    ----------
    model_name:
        sentence-transformers model identifier.  Defaults to the lightweight
        ``all-MiniLM-L6-v2`` (384-dim, ~80 MB, runs on CPU).
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._encoder: LocalEncoder = get_encoder(model_name)

    def build(self, job_description: str, title: str = "") -> RoleProfile:
        """Return a RoleProfile for the given *job_description* text."""
        keywords = extract_top_keywords(job_description)
        domain = detect_domain(job_description)
        embedding: list[float] = self._encoder.encode(job_description).tolist()

        return RoleProfile(
            id=str(uuid.uuid4()),
            title=title.strip() or "Unknown Role",
            domain=domain,
            keywords=keywords,
            embedding=embedding,
            job_description=job_description,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
