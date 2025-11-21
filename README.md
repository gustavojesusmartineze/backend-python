# Python Backend Project structure

A modern, scalable backend built using **FastAPI**, **Async SQLAlchemy**, and **Clean Architecture with Vertical Slicing**.

---

# 🚀 Tech Stack

- **FastAPI** (async-first API framework)
- **Python 3.12**
- **SQLAlchemy 2.0 Async ORM**
- **Alembic (async migrations)**
- **PostgreSQL 16**
- **Pydantic v2**
- **Docker + docker-compose**
- **Caddy (reverse proxy)**

---

# 🏗 Project Architecture

Following **Clean Architecture**, **Screaming Architecture**, and **Vertical Slices**:

```
app/
core/ # Global domain entities + VOs
config/
shared/ # Shared services, exceptions, interfaces
infrastructure/ # DB, API setup, frameworks & adapters
features/ # Vertical slice
```

Each slice contains:

- models.py
- repository.py
- service.py   
- schemas.py
- router.py

---

# 🐳 Running the Project (Development)

### 1. Build and start the environment


```bash
docker compose -f docker-compose.dev.yml up --build
```

### 2. Check if the app is running

```
curl http://localhost:8000/api/health
```

Expected:
```
{"status":"ok"}
```

### 3. Apply database migrations

```
docker compose -f docker-compose.dev.yml run --rm alembic alembic upgrade head
```

# 🧪 Running tests

### Run all tests:
```
docker compose -f docker-compose.dev.yml run --rm app pytest
```

### Run only integration tests:
```
docker compose -f docker-compose.dev.yml run --rm app pytest tests/integration
```

### Run only e2e tests:
(ensure the app is running first)
```
docker compose -f docker-compose.dev.yml run --rm app pytest tests/e2e
```

# 🧪 API Documentation
After starting the app:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

# 🗺 System Documentation
- [ADR-0001: Why FastAPI](docs/ADR-0001-fastapi-choice.md)
- [System Overview](docs/system-overview.md)

# 🛠 Development Notes

- Hot reload enabled via Uvicorn
- Database URL passed via environment variables
- Uses async session handling with SQLAlchemy
- Router auto-loading planned for expansion

# 📬 Contact / Maintainer

- Gustavo Martinez
- Team Leader @ Park Street Imports
- Backend Engineer — PHP, Angular, Python