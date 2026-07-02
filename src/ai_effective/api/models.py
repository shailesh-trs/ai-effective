from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class BuildProfileRequest(BaseModel):
    job_description: str
    title: str = ""


class ProfileResponse(BaseModel):
    id: str
    title: str
    domain: str
    keywords: list[str]
    created_at: str
    job_description: str


class ScoreRequest(BaseModel):
    profile_id: str
    query: str


class ScoreResponse(BaseModel):
    score: float
    semantic_score: float
    keyword_score: float
    task_score: float
    matched_task_type: Optional[str]
    query: str
    profile_title: str
    domain: str
    label: str


class BatchScoreRequest(BaseModel):
    profile_id: str
    queries: list[str]


class BatchScoreItem(BaseModel):
    score: float
    semantic_score: float
    keyword_score: float
    task_score: float
    matched_task_type: Optional[str]
    query: str
    label: str


class BatchScoreResponse(BaseModel):
    results: list[BatchScoreItem]
