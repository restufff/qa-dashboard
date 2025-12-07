from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import require_api_key

router = APIRouter(prefix="/load-runs", tags=["load-runs"])


@router.post("/locust", response_model=schemas.LoadTestRunBase)
def ingest_locust_run(
    payload: schemas.LocustRunPayload,
    db: Session = Depends(get_db),
    api=Depends(require_api_key),  # 🔐 VALIDATE API KEY HERE
):
    """
    Store load test summary (Locust / any tool converted to LocustRunPayload format).
    Requires X-API-KEY header.
    """
    # 1. Validate project
    project = db.query(models.Project).get(payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2. Insert run record
    run = models.LoadTestRun(
        project_id=payload.project_id,
        name=payload.name,
        environment=payload.environment,
        build=payload.build,
        branch=payload.branch,
        triggered_by=payload.triggered_by,
        total_requests=payload.total_requests,
        total_failures=payload.total_failures,
        avg_response_time=payload.avg_response_time,
        p95_response_time=payload.p95_response_time,
        p99_response_time=payload.p99_response_time,
        max_response_time=payload.max_response_time,
        min_response_time=payload.min_response_time,
        requests_per_second=payload.requests_per_second,
        failure_rate=payload.failure_rate,
        duration_seconds=payload.duration_seconds,
        success_threshold_met=payload.success_threshold_met,
        started_at=payload.started_at,
        finished_at=payload.finished_at,
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


@router.get("", response_model=List[schemas.LoadTestRunBase])
def list_load_runs(
    project_id: int,
    db: Session = Depends(get_db),
    api=Depends(require_api_key),  # 🔐 VALIDATE API KEY
):
    """
    List all load test runs for a project.
    Requires API key header.
    """
    return (
        db.query(models.LoadTestRun)
        .filter(models.LoadTestRun.project_id == project_id)
        .order_by(models.LoadTestRun.created_at.desc())
        .all()
    )


@router.get("/{load_run_id}", response_model=schemas.LoadTestRunBase)
def get_load_run(
    load_run_id: int,
    db: Session = Depends(get_db),
    api=Depends(require_api_key),  # 🔐 VALIDATE API KEY
):
    """
    Retrieve detail of a single load test run.
    Requires API key.
    """
    run = db.query(models.LoadTestRun).get(load_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Load test run not found")
    return run
