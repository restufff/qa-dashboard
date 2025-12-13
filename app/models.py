from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    test_runs = relationship("TestRun", back_populates="project", cascade="all, delete-orphan")
    load_runs = relationship("LoadTestRun", back_populates="project", cascade="all, delete-orphan")

    # TestRail-like modules (already in your repo or future)
    test_suites = relationship("TestSuite", back_populates="project", cascade="all, delete-orphan")
    test_cases = relationship("TestCase", back_populates="project", cascade="all, delete-orphan")
    evidences = relationship("Evidence", back_populates="project", cascade="all, delete-orphan")


class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    environment = Column(String(100), nullable=True)
    build = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=True)
    triggered_by = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="unknown")  # passed/failed/mixed/unknown
    total = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="test_runs")
    cases = relationship("TestCaseResult", back_populates="test_run", cascade="all, delete-orphan")

    # ✅ Execution cases (manual execution like TestRail/Qase)
    run_cases = relationship("TestRunCase", back_populates="test_run", cascade="all, delete-orphan")


class TestCaseResult(Base):
    __tablename__ = "test_case_results"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False)
    name = Column(String(255), nullable=False)
    classname = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)  # passed/failed/skipped/error
    duration = Column(Float, nullable=True)
    message = Column(Text, nullable=True)

    test_run = relationship("TestRun", back_populates="cases")


class LoadTestRun(Base):
    __tablename__ = "load_test_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    environment = Column(String(100), nullable=True)
    build = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=True)
    triggered_by = Column(String(100), nullable=True)

    total_requests = Column(Integer, default=0)
    total_failures = Column(Integer, default=0)
    avg_response_time = Column(Float, nullable=True)
    p95_response_time = Column(Float, nullable=True)
    p99_response_time = Column(Float, nullable=True)
    max_response_time = Column(Float, nullable=True)
    min_response_time = Column(Float, nullable=True)
    requests_per_second = Column(Float, nullable=True)
    failure_rate = Column(Float, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    success_threshold_met = Column(Boolean, default=None)

    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="load_runs")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    key = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==============================
# TestRail-like: Suites & Cases
# ==============================

class TestSuite(Base):
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="test_suites")
    test_cases = relationship("TestCase", back_populates="suite", cascade="all, delete-orphan")


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    suite_id = Column(Integer, ForeignKey("test_suites.id"), nullable=True)

    title = Column(String(255), nullable=False)
    preconditions = Column(Text, nullable=True)
    steps = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True)
    priority = Column(String(50), nullable=True)
    automation_type = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="test_cases")
    suite = relationship("TestSuite", back_populates="test_cases")

    run_cases = relationship("TestRunCase", back_populates="test_case", cascade="all, delete-orphan")
    evidences = relationship("Evidence", back_populates="test_case", cascade="all, delete-orphan")


# ==============================
# ✅ Execution: TestRunCase
# ==============================

class TestRunCase(Base):
    __tablename__ = "test_run_cases"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False)

    status = Column(String(50), nullable=False, default="untested")  # untested/passed/failed/blocked
    comment = Column(Text, nullable=True)
    executed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    test_run = relationship("TestRun", back_populates="run_cases")
    test_case = relationship("TestCase", back_populates="run_cases")


# ==============================
# Evidence (Drive link for now)
# ==============================

class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=True)
    test_run_case_id = Column(Integer, ForeignKey("test_run_cases.id"), nullable=True)

    file_name = Column(String(255), nullable=False)
    drive_file_id = Column(String(255), nullable=True)
    web_view_link = Column(Text, nullable=True)
    mime_type = Column(String(120), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="evidences")
    test_case = relationship("TestCase", back_populates="evidences")
