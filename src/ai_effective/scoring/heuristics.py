"""Pure-Python heuristics for TAS sub-scores.

No model calls, no external libraries beyond the standard library.
"""

from __future__ import annotations

from ai_effective.role_profile.extractor import tokenize
from ai_effective.role_profile.taxonomy import ROLE_TAXONOMY

# Cosine similarity thresholds calibrated to all-MiniLM-L6-v2 output ranges.
# Raw cosine for unrelated texts ≈ 0.0-0.15; same-domain ≈ 0.3-0.65.
_SEM_LOW = 0.05   # below this → semantic score = 0
_SEM_HIGH = 0.55  # above this → semantic score = 1.0


def scale_cosine(raw: float) -> float:
    """Map raw cosine similarity to [0, 1] using calibrated thresholds."""
    scaled = (raw - _SEM_LOW) / (_SEM_HIGH - _SEM_LOW)
    return max(0.0, min(1.0, scaled))


def keyword_overlap_score(query: str, role_keywords: list[str]) -> float:
    """Fraction of role keywords present in the query, capped at 1.0.

    Matching 5 or more role keywords returns a full score.  Both single-word
    and multi-word keywords are checked.
    """
    if not role_keywords:
        return 0.0

    query_tokens = set(tokenize(query))
    query_lower = query.lower()

    matched = 0
    for kw in role_keywords:
        if " " in kw:
            if kw in query_lower:
                matched += 1
        elif kw in query_tokens:
            matched += 1

    return min(1.0, matched / 5.0)


def task_type_score(query: str, domain: str) -> tuple[float, str | None]:
    """Score query alignment with expected task types for *domain*.

    Returns ``(score, best_task_type_name)``.

    Requires at least 2 keyword hits to register as a real match; a single
    hit is treated as noise.  This prevents generic verbs like "write" from
    inflating the score when the query topic is unrelated to the role.
    """
    if domain not in ROLE_TAXONOMY:
        return 0.5, None

    task_kws = ROLE_TAXONOMY[domain]["task_keywords"]
    query_lower = query.lower()

    best_score = 0.0
    best_task: str | None = None

    for task_type, keywords in task_kws.items():
        if not keywords:
            continue

        hits = sum(1 for kw in keywords if kw in query_lower)

        if hits < 2:
            # Single-keyword match is weak signal — score it very low.
            score = 0.1 * hits
        else:
            # Denominator: 30 % of keyword list, at least 2.
            denom = max(2.0, len(keywords) * 0.30)
            score = min(1.0, hits / denom)

        if score > best_score:
            best_score = score
            best_task = task_type

    return best_score, best_task
