from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/test-runs", tags=["test-runs"])


@router.get("", response_model=List[schemas.TestRunBase])
def list_test_runs(project_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.TestRun)
        .filter(models.TestRun.project_id == project_id)
        .order_by(models.TestRun.created_at.desc())
        .all()
    )


@router.get("/{run_id}", response_model=schemas.TestRunBase)
def get_test_run(run_id: int, db: Session = Depends(get_db)):
    tr = db.query(models.TestRun).get(run_id)
    if not tr:
        raise HTTPException(status_code=404, detail="Test run not found")
    return tr


# ==========================
# ✅ EXECUTION CASES
# ==========================

@router.get("/{run_id}/cases", response_model=List[schemas.TestRunCaseWithTestCase])
def list_run_cases(run_id: int, db: Session = Depends(get_db)):
    tr = db.query(models.TestRun).get(run_id)
    if not tr:
        raise HTTPException(status_code=404, detail="Test run not found")

    run_cases = (
        db.query(models.TestRunCase)
        .options(joinedload(models.TestRunCase.test_case))
        .filter(models.TestRunCase.test_run_id == run_id)
        .order_by(models.TestRunCase.id.asc())
        .all()
    )
    return run_cases


@router.post("/{run_id}/cases", response_model=List[schemas.TestRunCaseWithTestCase])
def generate_run_cases(run_id: int, payload: List[schemas.TestRunCaseCreate], db: Session = Depends(get_db)):
    tr = db.query(models.TestRun).get(run_id)
    if not tr:
        raise HTTPException(status_code=404, detail="Test run not found")

    # Validate test cases belong to same project
    for item in payload:
        tc = db.query(models.TestCase).get(item.test_case_id)
        if not tc or tc.project_id != tr.project_id:
            raise HTTPException(status_code=400, detail="Invalid test_case_id for this run")

        exists = (
            db.query(models.TestRunCase)
            .filter(models.TestRunCase.test_run_id == run_id, models.TestRunCase.test_case_id == item.test_case_id)
            .first()
        )
        if not exists:
            db.add(models.TestRunCase(
                test_run_id=run_id,
                test_case_id=item.test_case_id,
                status="untested"
            ))

    db.commit()

    run_cases = (
        db.query(models.TestRunCase)
        .options(joinedload(models.TestRunCase.test_case))
        .filter(models.TestRunCase.test_run_id == run_id)
        .order_by(models.TestRunCase.id.asc())
        .all()
    )
    return run_cases


@router.put("/cases/{run_case_id}", response_model=schemas.TestRunCaseBase)
def update_run_case(run_case_id: int, payload: schemas.TestRunCaseUpdate, db: Session = Depends(get_db)):
    rc = db.query(models.TestRunCase).get(run_case_id)
    if not rc:
        raise HTTPException(status_code=404, detail="Run case not found")

    # Update
    rc.status = payload.status
    rc.comment = payload.comment
    rc.executed_at = datetime.utcnow()
    rc.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(rc)
    return rc
