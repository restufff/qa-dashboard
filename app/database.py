from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Gunakan path absolut supaya tidak nyasar ke folder lain
DATABASE_URL = "sqlite:///G:/dashboard-qa/qops.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # wajib untuk SQLite + FastAPI
    echo=True,  # sementara untuk debug SQL, nanti bisa dimatikan
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print("FULL DB PATH:", os.path.abspath("G:/dashboard-qa/qops.db"))


def get_db():
    """
    Dependency untuk mendapatkan session DB per-request.
    Commit/rollback DIURUS di dalam route, bukan di sini.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
