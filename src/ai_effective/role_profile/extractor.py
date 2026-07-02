"""Text preprocessing, keyword extraction, and role domain detection.

All pure Python — no external NLP library or API calls required.
"""

from __future__ import annotations

import re
from collections import Counter

from ai_effective.role_profile.taxonomy import ROLE_TAXONOMY

# Broad English stopword list (avoids an nltk corpus download).
_STOPWORDS: frozenset[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "can", "shall", "must",
    "this", "that", "these", "those", "i", "you", "he", "she", "we", "they",
    "it", "its", "our", "your", "their", "my", "his", "her", "who", "what",
    "which", "when", "where", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "same", "so", "than", "too", "very", "about", "above", "after", "also",
    "back", "before", "between", "even", "first", "here", "into", "just",
    "like", "long", "make", "many", "much", "new", "next", "now", "over",
    "own", "right", "see", "still", "take", "think", "through", "time",
    "under", "well", "within", "without", "work", "year", "use", "using",
    "get", "set", "run", "need", "want", "able", "ensure", "provide",
    "experience", "strong", "excellent", "good", "great", "required",
    "preferred", "including", "ability", "skills", "knowledge",
    "understanding", "team", "cross", "functional", "day", "s", "t", "d",
    "re", "ll", "ve", "help", "us", "one", "two", "three", "per", "key",
    "must", "looking", "role", "join", "opportunity", "position", "job",
    "responsible", "responsibilities", "requirements", "qualification",
    "qualifications", "ideal", "candidate", "work", "working",
})


def tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, split on whitespace, remove stopwords."""
    text = text.lower()
    text = re.sub(r"[^\w\s/-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    tokens = []
    for raw in text.split():
        token = raw.strip("-/")
        if len(token) > 2 and token not in _STOPWORDS:
            tokens.append(token)
    return tokens


def extract_top_keywords(text: str, top_n: int = 40) -> list[str]:
    """Return the top-N most frequent content words from *text*."""
    freq = Counter(tokenize(text))
    return [word for word, _ in freq.most_common(top_n)]


def detect_domain(text: str) -> str:
    """Return the best-matching role domain by taxonomy keyword overlap.

    Falls back to ``"general"`` when no domain scores above zero.
    """
    text_lower = text.lower()
    scores: dict[str, int] = {}

    for domain, config in ROLE_TAXONOMY.items():
        count = sum(1 for kw in config["keywords"] if kw in text_lower)
        scores[domain] = count

    best_score = max(scores.values(), default=0)
    if best_score == 0:
        return "general"

    return max(scores, key=lambda d: scores[d])
