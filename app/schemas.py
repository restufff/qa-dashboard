from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# =========================
# PROJECTS
# =========================

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# TEST CASE RESULTS
# =========================

class TestCaseResultBase(BaseModel):
    id: int
    name: str
    classname: Optional[str]
    status: str
    duration: Optional[float]
    message: Optional[str]

    class Config:
        from_attributes = True


# =========================
# TEST RUN
# =========================

class TestRunBase(BaseModel):
    id: int
    project_id: int
    name: str
    environment: Optional[str]
    build: Optional[str]
    branch: Optional[str]
    triggered_by: Optional[str]
    status: str
    total: int
    passed: int
    failed: int
    skipped: int
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class TestRunDetail(TestRunBase):
    cases: List[TestCaseResultBase]

    class Config:
        from_attributes = True


# =========================
# PAYLOAD FOR ROBOT RUN
# =========================

class RobotRunMeta(BaseModel):
    project_id: int
    name: str = "robot-run"
    environment: Optional[str] = None
    build: Optional[str] = None
    branch: Optional[str] = None
    triggered_by: Optional[str] = None


# =========================
# LOAD TEST RUN
# =========================

class LoadTestRunBase(BaseModel):
    id: int
    project_id: int
    name: str
    environment: Optional[str]
    build: Optional[str]
    branch: Optional[str]
    triggered_by: Optional[str]
    total_requests: int
    total_failures: int
    avg_response_time: Optional[float]
    p95_response_time: Optional[float]
    p99_response_time: Optional[float]
    max_response_time: Optional[float]
    min_response_time: Optional[float]
    requests_per_second: Optional[float]
    failure_rate: Optional[float]
    duration_seconds: Optional[float]
    success_threshold_met: Optional[bool]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class LocustRunPayload(BaseModel):
    project_id: int
    name: str = "locust-run"
    environment: Optional[str] = None
    build: Optional[str] = None
    branch: Optional[str] = None
    triggered_by: Optional[str] = None

    total_requests: int
    total_failures: int
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    max_response_time: float
    min_response_time: float
    requests_per_second: float
    failure_rate: float
    duration_seconds: float

    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    success_threshold_met: Optional[bool] = None

    extra: Optional[Dict[str, Any]] = None


# =========================
# API KEY MODEL
# =========================

class APIKeyBase(BaseModel):
    id: int
    name: str
    key: str
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeyCreate(BaseModel):
    name: str


# =========================
# SUMMARY DASHBOARD MODEL
# =========================

class ProjectSummary(BaseModel):
    project: ProjectBase
    last_test_run: Optional[TestRunBase]
    last_load_run: Optional[LoadTestRunBase]
    overall_pass_rate: Optional[float]
    last_load_failure_rate: Optional[float]

    class Config:
        from_attributes = True
