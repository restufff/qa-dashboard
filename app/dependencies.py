from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import APIKey

def require_api_key(x_api_key: str = Header(None), db: Session = Depends(get_db)):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API Key")

    rec = db.query(APIKey).filter(APIKey.key == x_api_key).first()

    if not rec:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return rec
