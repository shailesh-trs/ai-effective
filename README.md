# ai-effective

> **AI Usage Efficiency Score (AUES)** — open-source Python library + web UI for measuring how well employees use AI relative to their actual job roles.
>
> **Zero frontier LLM calls.** All scoring runs locally using a small sentence-transformer model (~80 MB, CPU-only) plus pure-Python heuristics.

---

## What Is This?

Enterprise AI governance tools can tell you *that* AI was used, *how many tokens* it consumed, and *whether the output was factually correct*.  
None of them answer: **"Was this AI interaction a good use of this employee's time and their employer's money, given their actual job?"**

`ai-effective` fills that gap with the **Task Alignment Score (TAS)** — the first component of the full AUES metric.

---

## Task Alignment Score (TAS)

TAS scores 0–100 and measures whether a user's AI query aligns with their role profile.

| Component | Weight | What it measures |
|---|---|---|
| **Semantic alignment** | 50% | Cosine similarity between the query and the role-profile embedding |
| **Keyword overlap** | 30% | How many role-specific terms appear in the query |
| **Task-type match** | 20% | Does the query match a task type expected for this role (e.g. "debugging" for an SWE)? |

### Score labels

| Range | Label | Interpretation |
|---|---|---|
| 75–100 | High | Clearly work-relevant query |
| 50–74 | Medium | Partially relevant |
| 25–49 | Low | Tangential to the role |
| 0–24 | Very Low | Unrelated to the role |

### Role domains supported

`software_engineering` · `data_science` · `product_management` · `marketing` · `finance` · `hr_people` · `legal_compliance` · `design_ux` · `devops_infrastructure` · `operations`

---

## Project Structure

```
ai-effective/
├── src/
│   └── ai_effective/
│       ├── embeddings/
│       │   └── encoder.py          # LocalEncoder — wraps sentence-transformers
│       ├── role_profile/
│       │   ├── taxonomy.py         # 10 role domains with task-type keyword maps
│       │   ├── extractor.py        # tokenisation, keyword extraction, domain detection
│       │   └── builder.py          # RoleProfile dataclass + RoleProfileBuilder
│       ├── scoring/
│       │   ├── heuristics.py       # keyword overlap, cosine scaling, task-type scoring
│       │   └── tas.py              # TASScorer + TASResult
│       ├── api/
│       │   ├── models.py           # Pydantic request/response schemas
│       │   └── server.py           # FastAPI application
│       ├── store.py                # JSON-on-disk profile persistence (~/.ai-effective/)
│       └── cli.py                  # Click CLI (ai-effective command)
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── RoleProfileBuilder.jsx
│           ├── TASScorer.jsx
│           └── ScoreDisplay.jsx
├── pyproject.toml
└── requirements.txt
```

---

## Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/shailesh-trs/ai-effective.git
cd ai-effective

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# Install the package (editable mode)
pip install -e .
```

The first run downloads `all-MiniLM-L6-v2` (~80 MB) and caches it via Hugging Face Hub.

---

### 2. Use the CLI

**Build a role profile from a job description:**

```bash
# Inline description
ai-effective profile build -t "Senior Software Engineer" -d "We are looking for a Python backend engineer..."

# From a file
ai-effective profile build -t "Data Scientist" -f job_description.txt

# Opens $EDITOR if no -d or -f given
ai-effective profile build -t "Product Manager"
```

**List saved profiles:**

```bash
ai-effective profile list
```

**Score a query:**

```bash
ai-effective score -p <profile-id-prefix> -q "Help me write a binary search algorithm in Python"
```

Example output:

```
╭─ TAS — Senior Software Engineer ──────────────────────────╮
│ TAS Score:  72.4 / 100  (medium)                          │
│                                                            │
│   Semantic alignment  (50 %)    68.2                       │
│   Keyword overlap     (30 %)    80.0                       │
│   Task-type match     (20 %)    66.7                       │
│                                                            │
│ Matched task type:  code_generation                        │
│ Role domain:        software_engineering                   │
╰────────────────────────────────────────────────────────────╯
```

---

### 3. Launch the Web UI

```bash
# Start backend API (auto-opens browser to localhost:8000)
ai-effective serve

# Or on a custom port
ai-effective serve --port 8080 --no-browser
```

Then in a second terminal, start the frontend dev server:

```bash
cd frontend
npm install
npm run dev          # → http://localhost:5173
```

> **Production build:** `cd frontend && npm run build`  
> FastAPI will serve the built files automatically from `frontend/dist/`.

API docs: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---

## Python Library Usage

```python
from ai_effective import RoleProfileBuilder, TASScorer
from ai_effective.store import ProfileStore

# Build a role profile (downloads model on first run, then cached)
builder = RoleProfileBuilder()
profile = builder.build(
    job_description=open("jd.txt").read(),
    title="Senior Data Scientist"
)

# Persist it to ~/.ai-effective/profiles/
ProfileStore().save(profile)

# Score a query
scorer = TASScorer()
result = scorer.score(profile, "Help me build a classification model for churn prediction")

print(result.score)              # e.g. 81.3
print(result.label)              # "high"
print(result.semantic_score)     # 76.4
print(result.keyword_score)      # 100.0
print(result.task_score)         # 66.7
print(result.matched_task_type)  # "model_building"

# Batch scoring
results = scorer.score_batch(profile, ["query 1", "query 2", ...])
```

---

## REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/profiles` | Build and save a role profile |
| `GET` | `/api/profiles` | List all saved profiles |
| `GET` | `/api/profiles/{id}` | Get a single profile |
| `DELETE` | `/api/profiles/{id}` | Delete a profile |
| `POST` | `/api/score` | Score a single query |
| `POST` | `/api/score/batch` | Score multiple queries |

Full schema at `/api/docs` (Swagger UI).

---

## How TAS Works (No LLMs)

### Role Profile Builder

1. **Keyword extraction** — tokenise the job description, strip stopwords, rank by frequency → top 40 content words become the profile's keyword fingerprint.
2. **Domain detection** — count keyword overlaps between the job description and each of the 10 taxonomy domains → assign the best match.
3. **Embedding** — encode the full job description with `all-MiniLM-L6-v2` (384-dim, L2-normalised). Stored as a JSON list alongside the keywords.

### TAS Scorer

1. **Semantic alignment** — encode the query, dot-product with the role embedding (= cosine similarity for L2-normalised vectors). Mapped to [0, 1] using calibrated thresholds for the MiniLM output range.
2. **Keyword overlap** — count how many profile keywords appear in the query. 5 matches = full score; caps at 1.0.
3. **Task-type match** — for each expected task type in the domain, count detection-phrase hits in the query. Requires ≥ 2 hits to count as a real match (prevents single generic verbs from inflating the score).

All three components are independently interpretable, so low scores tell you exactly which lever to pull.

---

## Roadmap

- [ ] Session-level TAS — aggregate across a full conversation log
- [ ] Full AUES metric — Prompt Quality Score (PQS), Output Engagement Score (OES), Utility Score (US)
- [ ] Langfuse plugin — emit TAS as evaluation metrics
- [ ] Weekly digest — personal AI usage report card
- [ ] Prompt Registry — version-controlled, role-indexed prompt library

---

## Contributing

Issues and PRs welcome. The taxonomy (`src/ai_effective/role_profile/taxonomy.py`) is data-only — adding a new role domain is a few lines of Python.

---

## License

MIT
