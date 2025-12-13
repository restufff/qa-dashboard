from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/test-cases",
    tags=["test-cases"],
    # Kalau mau pakai API key protection:
    # dependencies=[Depends(require_api_key)]
)


@router.post("", response_model=schemas.TestCaseBase)
def create_test_case(
    payload: schemas.TestCaseCreate,
    db: Session = Depends(get_db),
):
    # pastikan project exist
    project = db.query(models.Project).get(payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # kalau ada suite_id, pastikan suite-nya milik project yang sama
    suite = None
    if payload.suite_id is not None:
        suite = db.query(models.TestSuite).get(payload.suite_id)
        if not suite or suite.project_id != payload.project_id:
            raise HTTPException(status_code=400, detail="Invalid suite_id for this project")

    now = datetime.utcnow()
    case = models.TestCase(
        project_id=payload.project_id,
        suite_id=payload.suite_id,
        title=payload.title,
        preconditions=payload.preconditions,
        steps=payload.steps,
        expected_result=payload.expected_result,
        priority=payload.priority,
        automation_type=payload.automation_type,
        created_at=now,
        updated_at=now,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get("", response_model=List[schemas.TestCaseBase])
def list_test_cases(
    project_id: int = Query(..., description="Filter by project_id"),
    suite_id: Optional[int] = Query(None, description="Optional: filter by suite_id"),
    db: Session = Depends(get_db),
):
    q = db.query(models.TestCase).filter(models.TestCase.project_id == project_id)
    if suite_id is not None:
        q = q.filter(models.TestCase.suite_id == suite_id)

    return q.order_by(models.TestCase.created_at.desc()).all()


@router.get("/{case_id}", response_model=schemas.TestCaseBase)
def get_test_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.TestCase).get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Test case not found")
    return case


@router.put("/{case_id}", response_model=schemas.TestCaseBase)
def update_test_case(
    case_id: int,
    payload: schemas.TestCaseUpdate,
    db: Session = Depends(get_db),
):
    case = db.query(models.TestCase).get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Test case not found")

    # update field kalau tidak None
    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(case, field, value)

    case.updated_at = datetime.utcnow()
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.delete("/{case_id}", status_code=204)
def delete_test_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.TestCase).get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Test case not found")

    db.delete(case)
    db.commit()
    return None
