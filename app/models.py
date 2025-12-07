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


class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    environment = Column(String(100), nullable=True)
    build = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=True)
    triggered_by = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="unknown")  # passed/failed/mixed
    total = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="test_runs")
    cases = relationship("TestCaseResult", back_populates="test_run", cascade="all, delete-orphan")


class TestCaseResult(Base):
    __tablename__ = "test_case_results"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False)
    name = Column(String(255), nullable=False)
    classname = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)  # passed/failed/skipped/error
    duration = Column(Float, nullable=True)      # in seconds
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
    failure_rate = Column(Float, nullable=True)  # 0-100
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