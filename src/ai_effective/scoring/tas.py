"""Task Alignment Score (TAS) — the core AUES sub-metric.

TAS answers: "Was this AI query relevant to the user's actual job?"

Score = 0-100, composed of three independently interpretable signals:

  Component            Weight  What it measures
  ───────────────────  ──────  ──────────────────────────────────────────────
  Semantic alignment    50 %   Cosine similarity between the query and the
                               role-profile embedding (local model, no API).
  Keyword overlap       30 %   How many role-specific terms appear in query.
  Task-type match       20 %   Does the query match a task type typical for
                               this role domain (e.g. "debugging" for SWE)?

No frontier LLM calls — all inference uses the cached LocalEncoder.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ai_effective.embeddings.encoder import LocalEncoder, get_encoder
from ai_effective.role_profile.builder import RoleProfile
from ai_effective.scoring.heuristics import (
    keyword_overlap_score,
    scale_cosine,
    task_type_score,
)

_SEMANTIC_W = 0.50
_KEYWORD_W = 0.30
_TASK_W = 0.20


@dataclass
class TASResult:
    score: float               # 0-100
    semantic_score: float      # 0-100
    keyword_score: float       # 0-100
    task_score: float          # 0-100
    matched_task_type: str | None
    query: str
    profile_title: str
    domain: str

    @property
    def label(self) -> str:
        if self.score >= 75:
            return "high"
        if self.score >= 50:
            return "medium"
        if self.score >= 25:
            return "low"
        return "very_low"


class TASScorer:
    """Score a user query against a RoleProfile.

    Parameters
    ----------
    model_name:
        sentence-transformers model.  Must match the one used to build the
        profile so embedding spaces are aligned.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._encoder: LocalEncoder = get_encoder(model_name)

    def score(self, profile: RoleProfile, query: str) -> TASResult:
        """Compute TAS for a single *query* against *profile*."""
        # 1. Semantic: dot product of L2-normalised embeddings = cosine similarity
        query_emb = self._encoder.encode(query)
        role_emb = profile.embedding_array()
        cos_sim = float(np.dot(role_emb, query_emb))
        semantic = scale_cosine(cos_sim)

        # 2. Keyword overlap
        kw = keyword_overlap_score(query, profile.keywords)

        # 3. Task-type match
        task, matched_task = task_type_score(query, profile.domain)

        # 4. Weighted sum → 0-100
        raw = _SEMANTIC_W * semantic + _KEYWORD_W * kw + _TASK_W * task
        tas = round(raw * 100, 1)

        return TASResult(
            score=tas,
            semantic_score=round(semantic * 100, 1),
            keyword_score=round(kw * 100, 1),
            task_score=round(task * 100, 1),
            matched_task_type=matched_task,
            query=query,
            profile_title=profile.title,
            domain=profile.domain,
        )

    def score_batch(self, profile: RoleProfile, queries: list[str]) -> list[TASResult]:
        """Score multiple queries against the same profile."""
        return [self.score(profile, q) for q in queries]
