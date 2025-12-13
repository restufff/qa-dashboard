from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/evidences",
    tags=["evidences"],
    # dependencies=[Depends(require_api_key)]
)


@router.post("", response_model=schemas.EvidenceBase)
def create_evidence(
    payload: schemas.EvidenceCreate,
    db: Session = Depends(get_db),
):
    # pastikan project exist
    project = db.query(models.Project).get(payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # validasi optional test_run & test_case
    if payload.test_run_id is not None:
        run = db.query(models.TestRun).get(payload.test_run_id)
        if not run or run.project_id != payload.project_id:
            raise HTTPException(status_code=400, detail="Invalid test_run_id for this project")

    if payload.test_case_id is not None:
        case = db.query(models.TestCase).get(payload.test_case_id)
        if not case or case.project_id != payload.project_id:
            raise HTTPException(status_code=400, detail="Invalid test_case_id for this project")

    evidence = models.Evidence(
        project_id=payload.project_id,
        test_run_id=payload.test_run_id,
        test_case_id=payload.test_case_id,
        drive_file_id=payload.drive_file_id,
        file_name=payload.file_name,
        mime_type=payload.mime_type,
        web_view_link=payload.web_view_link,
        web_content_link=payload.web_content_link,
        uploaded_by=payload.uploaded_by,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


@router.get("/by-run/{test_run_id}", response_model=List[schemas.EvidenceBase])
def list_evidences_by_run(
    test_run_id: int,
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Evidence).filter(models.Evidence.test_run_id == test_run_id)
    if project_id is not None:
        q = q.filter(models.Evidence.project_id == project_id)
    return q.order_by(models.Evidence.created_at.desc()).all()


@router.get("/by-case/{test_case_id}", response_model=List[schemas.EvidenceBase])
def list_evidences_by_case(
    test_case_id: int,
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Evidence).filter(models.Evidence.test_case_id == test_case_id)
    if project_id is not None:
        q = q.filter(models.Evidence.project_id == project_id)
    return q.order_by(models.Evidence.created_at.desc()).all()

@router.delete("/{evidence_id}", status_code=204)
def delete_evidence(evidence_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Evidence).get(evidence_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Evidence not found")

    db.delete(obj)
    db.commit()
    return None