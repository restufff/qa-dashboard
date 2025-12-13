from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# ==== PROJECTS ==== #

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


# ==== TEST RUNS (Robot/JUnit ingestion) ==== #

class TestCaseResultBase(BaseModel):
    id: int
    name: str
    classname: Optional[str]
    status: str
    duration: Optional[float]
    message: Optional[str]

    class Config:
        from_attributes = True


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


class RobotRunMeta(BaseModel):
    project_id: int
    name: str = "robot-run"
    environment: Optional[str] = None
    build: Optional[str] = None
    branch: Optional[str] = None
    triggered_by: Optional[str] = None


# ==== LOAD TEST RUNS ==== #

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


# ==== DASHBOARD SUMMARY ==== #

class ProjectSummary(BaseModel):
    project: ProjectBase
    last_test_run: Optional[TestRunBase]
    last_load_run: Optional[LoadTestRunBase]
    overall_pass_rate: Optional[float]
    last_load_failure_rate: Optional[float]


# ==== API KEYS ==== #

class APIKeyBase(BaseModel):
    id: int
    name: str
    key: str
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeyCreate(BaseModel):
    name: str


# ============================
# TestRail-like: Suites/Cases
# ============================

class TestSuiteCreate(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None


class TestSuiteBase(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TestCaseCreate(BaseModel):
    project_id: int
    suite_id: Optional[int] = None
    title: str
    preconditions: Optional[str] = None
    steps: Optional[str] = None
    expected_result: Optional[str] = None
    priority: Optional[str] = None
    automation_type: Optional[str] = None


class TestCaseUpdate(BaseModel):
    suite_id: Optional[int] = None
    title: Optional[str] = None
    preconditions: Optional[str] = None
    steps: Optional[str] = None
    expected_result: Optional[str] = None
    priority: Optional[str] = None
    automation_type: Optional[str] = None


class TestCaseBase(BaseModel):
    id: int
    project_id: int
    suite_id: Optional[int]
    title: str
    preconditions: Optional[str]
    steps: Optional[str]
    expected_result: Optional[str]
    priority: Optional[str]
    automation_type: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================
# ✅ Execution: TestRunCase
# ============================

class TestRunCaseBase(BaseModel):
    id: int
    test_run_id: int
    test_case_id: int
    status: str
    comment: Optional[str]
    executed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TestRunCaseCreate(BaseModel):
    test_case_id: int


class TestRunCaseUpdate(BaseModel):
    status: str
    comment: Optional[str] = None


class TestRunCaseWithTestCase(TestRunCaseBase):
    test_case: TestCaseBase


# ============================
# Evidence
# ============================

class EvidenceCreate(BaseModel):
    project_id: int
    test_case_id: Optional[int] = None
    test_run_case_id: Optional[int] = None
    file_name: str
    drive_file_id: Optional[str] = None
    web_view_link: Optional[str] = None
    mime_type: Optional[str] = None


class EvidenceBase(BaseModel):
    id: int
    project_id: int
    test_case_id: Optional[int]
    test_run_case_id: Optional[int]
    file_name: str
    drive_file_id: Optional[str]
    web_view_link: Optional[str]
    mime_type: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
