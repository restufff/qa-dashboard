# Recommended Files to Add to Repository

## Essential Files (Priority: HIGH)

### 1. `.env.example`

Template environment variables file untuk development dan production setup.

```
DATABASE_URL=sqlite:///./qops.db
# DATABASE_URL=postgresql://user:password@localhost/qops
API_KEY_SECRET_KEY=your-secret-key-here
DEBUG=False
LOG_LEVEL=info
```

### 2. `docker-compose.yml` (if using containers)

Local development database setup (PostgreSQL recommended for production).

### 3. `setup.sh` / `setup.ps1` (Installation script)

Script untuk quick setup environment dan dependencies.

### 4. `.dockerignore`

Optimize Docker builds (should mirror .gitignore items).

### 5. `CONTRIBUTING.md`

Guidelines untuk contributors.

### 6. `CHANGELOG.md`

Document perubahan versi.

---

## Development Files (Priority: MEDIUM)

### 7. `conftest.py`

Pytest configuration dan fixtures untuk testing.

### 8. `.env.test`

Environment variables khusus untuk testing.

### 9. `pytest.ini`

Pytest configuration file.

### 10. `pyproject.toml` (atau `setup.cfg`)

Modern Python project configuration (replace/supplement requirements.txt).

### 11. `Makefile` atau `justfile`

Handy commands untuk development tasks:

```make
.PHONY: install run test lint format

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	pylint app/

format:
	black app/
```

---

## CI/CD Files (Priority: MEDIUM)

### 12. `.github/workflows/tests.yml`

Automated testing on push/PR.

### 13. `.github/workflows/lint.yml`

Code quality checks (linting, formatting).

### 14. `.github/workflows/docker-build.yml`

Automated Docker image building.

---

## Documentation Files (Priority: LOW)

### 15. `docs/API.md`

API documentation (atau reference ke /docs endpoint).

### 16. `docs/SETUP.md`

Detailed setup instructions.

### 17. `docs/DATABASE.md`

Database schema documentation.

---

## Additional Config Files (Priority: LOW)

### 18. `.pre-commit-config.yaml`

Automated code quality checks sebelum commit:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### 19. `.pylintrc` / `pyproject.toml [tool.pylint]`

Linting configuration.

### 20. `alembic/` directory

Database migration management (jika upgrade ke PostgreSQL/production DB).

---

## Current Issues to Fix

### Priority: HIGH

1. **Database Choice**: Currently using SQLite (`qops.db`).

   - Recommendation: Keep SQLite for development, PostgreSQL untuk production
   - Update `DATABASE_URL` handling di `database.py`

2. **API Key Security**:

   - Currently storing API keys in plaintext di database
   - Add hashing: `pip install bcrypt` dan update auth schema/model

3. **Missing Tests**:
   - Create `tests/` directory dengan unit tests
   - Create test fixtures untuk database

### Priority: MEDIUM

1. **Logging**: Add structured logging dengan `python-json-logger` atau `loguru`
2. **Validation**: Enhance Pydantic models dengan lebih strict validation
3. **Error Handling**: Add proper error handling dan custom exception classes
4. **Documentation**: Add docstrings ke semua functions/endpoints

---

## Recommended Directory Structure After Changes

```
dashboard-qa/
├── .github/
│   └── workflows/
│       ├── tests.yml
│       ├── lint.yml
│       └── docker-build.yml
├── app/
│   ├── routers/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_projects.py
│   │   └── test_runs.py
│   ├── __init__.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── docs/
│   ├── API.md
│   ├── SETUP.md
│   └── DATABASE.md
├── .env.example
├── .env.test
├── .gitignore (✓ DONE)
├── .pre-commit-config.yaml
├── .pylintrc
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md (existing - enhance)
├── requirements.txt (upgrade)
├── pyproject.toml
├── pytest.ini
├── CHANGELOG.md
├── CONTRIBUTING.md
├── setup.sh
└── setup.ps1
```

---

## Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # (need to create)

# Run
uvicorn app.main:app --reload

# Test
pytest

# Format
black app/
isort app/

# Lint
pylint app/
flake8 app/
```
