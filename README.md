# 🎓 EdTech Platform — Backend

A modern, scalable EdTech backend built using **FastAPI**, **Async SQLAlchemy**, and **Clean Architecture with Vertical Slicing**.

This backend powers modules for:

- Student information  
- Attendance tracking  
- Grade reporting  
- Curriculum & scheduling  
- Enrollment  
- Billing & payments  
- Internal messaging  
- Notifications  

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
src/
core/ # Global domain entities + VOs
common/ # Shared services, exceptions, interfaces
infrastructure/ # DB, API setup, frameworks & adapters
academic/ # Vertical slice: attendance, grades, curriculum
administrative/ # Enrollment, scheduling
communication/ # Messaging, notifications
financial/ # Billing, invoices, payments
```

Each slice contains:

- `domain/`
- `application/` (use cases)
- `interfaces.py`
- `api/` (routers)
- `repositories/` (infra overrides)

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