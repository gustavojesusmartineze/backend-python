# System Overview

## 1. Introduction

This document provides a high-level overview of the EdTech Platform backend, built with **FastAPI**, following **Clean Architecture**, **Vertical Slicing**, and **Screaming Architecture** principles.  
The system supports:

- School management (primary, secondary, academies)
- Attendance
- Grade reporting
- Scheduling
- Enrollment
- Billing & payments
- Messaging
- Notifications

---

## 2. Architecture Principles

### 2.1 Clean Architecture Layers

The project is structured into four main layers:

1. **Domain Layer (`core/` + slice-specific `domain/`)**  
   - Entities  
   - Value Objects  
   - Domain Rules  
   - Pure business logic  

2. **Application Layer (`application/`)**  
   - Use Cases  
   - DTOs  
   - Ports (interfaces)  

3. **Infrastructure Layer (`infrastructure/`)**  
   - Adapters (SQLAlchemy repositories, email providers, file storage)  
   - Database setup  
   - API framework (FastAPI)  

4. **Interface Layer (`api/`)**  
   - Routers  
   - Controllers  
   - Request/Response DTO models  

This separation ensures:

- High maintainability  
- Framework independence  
- Easy testability  
- Clear domain boundaries  

---

## 3. Screaming Architecture (Vertical Slices)

Instead of grouping code by technical layer alone, the system uses **business-first slicing**, making intentions clear from the top-level directory.

Example vertical slice layout:

```
academic/
attendance_control/
grade_reporting/
curriculum_config/

administrative/
enrollment_mgmt/
schedule_mgmt/

communication/
notifications/
internal_messaging/

financial/
invoice_generation/
payments/
```

Each slice contains:

- `domain/`  
- `application/`  
- `interfaces.py` (ports)  
- `api/` (routers/controllers)  
- `repositories/` (infrastructure overrides)  

This isolates business modules cleanly.

---

## 4. Technology Stack

- **Backend:** FastAPI (Python 3.12)  
- **Database:** PostgreSQL 16 + Async SQLAlchemy ORM  
- **Migrations:** Alembic (async)  
- **API Gateway:** Caddy  
- **Containerization:** Docker + docker-compose  
- **Async Driver:** asyncpg  
- **Validation:** Pydantic v2  
- **Logging:** Structured JSON logs (planned)

---

## 5. Database Architecture

The system uses:

- Async SQLAlchemy ORM for runtime operations  
- Sync engine for Alembic migrations  
- Automatic session management via dependency injection  

Database URL example:

```
postgresql+asyncpg://user:password@host:5432/dbname
```

---

## 6. API Overview

All API routes are grouped under:

/api/*


Examples:

- `/api/health`
- `/api/academic/attendance/...`
- `/api/administrative/enrollment/...`

Swagger Docs:  
http://localhost:8000/docs


---

## 7. Development Environment

### 7.1 Containers

- **app** (FastAPI runtime + Uvicorn reload)  
- **db** (PostgreSQL)  
- **alembic** (migration container)  
- **proxy** (Caddy reverse proxy)

### 7.2 Commands

Start environment:

```
docker compose -f docker-compose.dev.yml up --build
```

Apply database migrations:

```
docker compose -f docker-compose.dev.yml run --rm alembic alembic upgrade head
```


---

## 8. Future Directions

- Add Redis for background jobs  
- Add Celery or FastAPI BackgroundTasks  
- Add S3-based file storage  
- Implement authentication (JWT + refresh token rotation)  
- Add AI-based modules (recommendations, auto-grading assist, insights)

---

## 9. Conclusion

The EdTech backend is designed for scalable, long-term maintainability.  
Its architecture supports clear domain boundaries, modular business slices, and high performance under concurrency.

