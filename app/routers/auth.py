import secrets
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/api-key", response_model=schemas.APIKeyBase)
def create_api_key(payload: schemas.APIKeyCreate, db: Session = Depends(get_db)):
    key = secrets.token_hex(32)

    rec = models.APIKey(name=payload.name, key=key)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
