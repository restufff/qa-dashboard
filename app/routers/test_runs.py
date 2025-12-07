from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db
from ..dependencies import require_api_key

router = APIRouter(prefix="/test-runs", tags=["test-runs"])


@router.post("/robot", response_model=schemas.TestRunDetail)
async def ingest_robot_run(
    project_id: int = Form(...),
    name: str = Form("robot-run"),
    environment: str | None = Form(None),
    build: str | None = Form(None),
    branch: str | None = Form(None),
    triggered_by: str | None = Form(None),
    junit_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    api=Depends(require_api_key),  # API KEY VALIDATION
):
    """
    Endpoint upload report Robot Framework / pytest / JUnit XML.
    API key required via X-API-KEY header.
    """

    # 1. Validate project
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2. Read XML file
    xml_bytes = await junit_file.read()

    # 3. Parse XML → testcases + summary
    testcases_data, summary = utils.parse_junit_xml(xml_bytes)

    # 4. Determine status
    status = "unknown"
    if summary["total"] == 0:
        status = "unknown"
    elif summary["failed"] == 0:
        status = "passed"
    else:
        status = "failed"

    # 5. Store test run record
    test_run = models.TestRun(
        project_id=project.id,
        name=name,
        environment=environment,
        build=build,
        branch=branch,
        triggered_by=triggered_by,
        status=status,
        total=summary["total"],
        passed=summary["passed"],
        failed=summary["failed"],
        skipped=summary["skipped"],
    )
    db.add(test_run)
    db.flush()  # fetch test_run.id before commit

    # 6. Store testcase breakdown
    for tc in testcases_data:
        testcase = models.TestCaseResult(
            test_run_id=test_run.id,
            name=tc["name"],
            classname=tc["classname"],
            status=tc["status"],
            duration=tc["duration"],
            message=tc["message"],
        )
        db.add(testcase)

    # 7. Finalize commit
    db.commit()
    db.refresh(test_run)

    return test_run


@router.get("", response_model=List[schemas.TestRunBase])
def list_test_runs(
    project_id: int,
    db: Session = Depends(get_db),
    api=Depends(require_api_key),
):
    """
    List semua test run untuk project tertentu.
    API key required via header.
    """
    return (
        db.query(models.TestRun)
        .filter(models.TestRun.project_id == project_id)
        .order_by(models.TestRun.created_at.desc())
        .all()
    )


@router.get("/{test_run_id}", response_model=schemas.TestRunDetail)
def get_test_run(
    test_run_id: int,
    db: Session = Depends(get_db),
    api=Depends(require_api_key),
):
    """
    Ambil detail satu test run beserta hasil testcase.
    API key required.
    """
    test_run = db.query(models.TestRun).get(test_run_id)
    if not test_run:
        raise HTTPException(status_code=404, detail="Test run not found")
    return test_run
