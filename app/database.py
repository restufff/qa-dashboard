from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ganti ini ke PostgreSQL kalau mau
DATABASE_URL = "sqlite:///./qops.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency FastAPI untuk inject DB session di tiap request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
