from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=schemas.ProjectBase)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Cek duplicate berdasarkan name
    existing = (
        db.query(models.Project)
        .filter(models.Project.name == payload.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Project with this name already exists",
        )

    project = models.Project(
        name=payload.name,
        description=payload.description,
    )
    db.add(project)
    db.commit()          # ✅ COMMIT DI SINI
    db.refresh(project)  # ✅ Biar ID terisi

    print("DEBUG CREATED PROJECT:", project.id, project.name)

    return project


@router.get("", response_model=List[schemas.ProjectBase])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).order_by(models.Project.created_at.desc()).all()
