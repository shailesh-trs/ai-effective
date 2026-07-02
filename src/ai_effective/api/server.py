"""FastAPI application — all business logic lives in role_profile/ and scoring/."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from ai_effective.api.models import (
    BatchScoreRequest,
    BatchScoreResponse,
    BatchScoreItem,
    BuildProfileRequest,
    ProfileResponse,
    ScoreRequest,
    ScoreResponse,
)
from ai_effective.role_profile.builder import RoleProfileBuilder
from ai_effective.scoring.tas import TASScorer
from ai_effective.store import ProfileStore

app = FastAPI(title="AI Effective", version="0.1.0", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy singletons — the encoder model loads on first request.
_builder: RoleProfileBuilder | None = None
_scorer: TASScorer | None = None
_store = ProfileStore()


def _get_builder() -> RoleProfileBuilder:
    global _builder
    if _builder is None:
        _builder = RoleProfileBuilder()
    return _builder


def _get_scorer() -> TASScorer:
    global _scorer
    if _scorer is None:
        _scorer = TASScorer()
    return _scorer


def _profile_response(profile) -> ProfileResponse:
    d = profile.to_dict()
    d.pop("embedding", None)
    return ProfileResponse(**d)


# ── Health ─────────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


# ── Profiles ───────────────────────────────────────────────────────────────────

@app.post("/api/profiles", response_model=ProfileResponse, status_code=201)
def build_profile(req: BuildProfileRequest):
    if not req.job_description.strip():
        raise HTTPException(status_code=422, detail="job_description must not be empty")
    profile = _get_builder().build(req.job_description, req.title)
    _store.save(profile)
    return _profile_response(profile)


@app.get("/api/profiles", response_model=list[ProfileResponse])
def list_profiles():
    return [_profile_response(p) for p in _store.list_all()]


@app.get("/api/profiles/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: str):
    p = _store.load(profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return _profile_response(p)


@app.delete("/api/profiles/{profile_id}", status_code=200)
def delete_profile(profile_id: str):
    if not _store.delete(profile_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"deleted": True}


# ── Scoring ────────────────────────────────────────────────────────────────────

@app.post("/api/score", response_model=ScoreResponse)
def score_query(req: ScoreRequest):
    p = _store.load(req.profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    r = _get_scorer().score(p, req.query)
    return ScoreResponse(
        score=r.score,
        semantic_score=r.semantic_score,
        keyword_score=r.keyword_score,
        task_score=r.task_score,
        matched_task_type=r.matched_task_type,
        query=r.query,
        profile_title=r.profile_title,
        domain=r.domain,
        label=r.label,
    )


@app.post("/api/score/batch", response_model=BatchScoreResponse)
def score_batch(req: BatchScoreRequest):
    p = _store.load(req.profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    results = _get_scorer().score_batch(p, req.queries)
    return BatchScoreResponse(results=[
        BatchScoreItem(
            score=r.score,
            semantic_score=r.semantic_score,
            keyword_score=r.keyword_score,
            task_score=r.task_score,
            matched_task_type=r.matched_task_type,
            query=r.query,
            label=r.label,
        )
        for r in results
    ])


# ── Static frontend (built files) ──────────────────────────────────────────────

_frontend_dist = Path(__file__).resolve().parents[4] / "frontend" / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="ui")
