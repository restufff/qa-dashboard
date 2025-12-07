from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, get_db
from . import models, schemas
from .routers import projects, test_runs, load_runs, auth
from fastapi import Request

Base.metadata.create_all(bind=engine)

app = FastAPI(
    redirect_slashes=False,
    title="QOps Backend",
    description="Simple TestOps-like backend for functional + load testing",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # GUNAKAN * dulu saat development
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print("➡️ Incoming:", request.method, request.url)
    response = await call_next(request)
    print("⬅️ Response:", response.status_code)
    return response

app.include_router(projects.router)
app.include_router(test_runs.router)
app.include_router(load_runs.router)
app.include_router(auth.router)


@app.get("/projects/{project_id}/summary", response_model=schemas.ProjectSummary)
def get_project_summary(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    last_test_run = (
        db.query(models.TestRun)
        .filter(models.TestRun.project_id == project_id)
        .order_by(models.TestRun.created_at.desc())
        .first()
    )

    last_load_run = (
        db.query(models.LoadTestRun)
        .filter(models.LoadTestRun.project_id == project_id)
        .order_by(models.LoadTestRun.created_at.desc())
        .first()
    )

    overall_pass_rate = (
        (last_test_run.passed / last_test_run.total * 100.0)
        if (last_test_run and last_test_run.total and last_test_run.total > 0)
        else None
    )

    last_load_failure_rate = (
        last_load_run.failure_rate
        if (last_load_run and last_load_run.failure_rate is not None)
        else None
    )

    return schemas.ProjectSummary(
        project=project,
        last_test_run=last_test_run,
        last_load_run=last_load_run,
        overall_pass_rate=overall_pass_rate,
        last_load_failure_rate=last_load_failure_rate,
    )

