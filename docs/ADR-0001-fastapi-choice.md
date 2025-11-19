# ADR-0001: Adoption of FastAPI for Backend Application

**Status:** Accepted  
**Date:** 2025-11-20  
**Decision Makers:** Gustavo Martinez, Backend Architecture Team  
**Context:** EdTech Platform Backend (Institutions, Attendance, Grades, Billing, Communication)

---

## 1. Context

The EdTech platform backend requires:

- High concurrency & horizontal scalability  
- Clean Architecture alignment (domain-first, framework-last)  
- Strict separation between domain, application, and infrastructure layers  
- Native async support for I/O-bound operations  
- First-class developer experience  
- Strong ecosystem for validation, serialization, and API docs  
- Support for vertical slices & modular routers  
- Easy integration with PostgreSQL, Redis, background jobs, and AWS services

We evaluated three backend options:

| Option          | Pros | Cons |
|----------------|------|------|
| **Laravel (PHP)** | Familiar to existing team, batteries included, fast prototyping | No async I/O, less efficient for real-time + heavy I/O workloads, not ideal for deep Clean Architecture |
| **Node.js (Nest / Express)** | Good async model, large ecosystem | Weaker typing safety, DI and CA require more manual work |
| **FastAPI (Python)** | Async-first, type-safe, Pydantic models, clean DI, high performance, great for vertical slices, modern ecosystem | Team learning curve (Python + async) |

---

## 2. Decision

**We choose FastAPI as the primary backend framework for the EdTech platform.**

This decision is motivated by the need for:

- **Async-first architecture** for concurrency-heavy operations (attendance scans, messaging, batch grading, notifications)  
- **Type safety** via Pydantic models  
- **Performance** close to Node/Go for API serving  
- **Native support for dependency injection**  
- **Perfect alignment with Clean Architecture**  
- **Easy integration with async SQLAlchemy**  
- **Auto-generated interactive API documentation (OpenAPI/Swagger)**  
- **Built-in support for modular, vertical slicing router structure**

---

## 3. Consequences

### Positive
- Faster backend performance under load  
- Better maintainability via domain-driven folder structure  
- Clear contract-based DTOs using Pydantic  
- Easy orchestration through Docker + uv  
- Improved extensibility for microservices (notifications, billing, AI-driven analytics)

### Negative  
- Team must adopt Python + async/await syntax  
- More explicit configuration required than batteries-included frameworks  
- Alembic async migrations require careful setup

---

## 4. Alternatives Considered

1. **Laravel**  
   - Rejected due to lack of async and difficulty maintaining long-term high-concurrency modules.

2. **NestJS**  
   - Strong option, but FastAPI’s typing + DI are more elegant and simpler for Clean Architecture.

3. **Django / Django REST Framework**  
   - Too monolithic for vertical slices; async support still maturing.

---

## 5. Outcome

FastAPI is adopted as the backend foundation, combined with:

- SQLAlchemy Async ORM  
- Alembic async migrations  
- Clean Architecture + Domain-Driven principles  
- Vertical Slices + Screaming Architecture  
- Docker-based dev + Caddy reverse proxy  
- Future-ready for AI integrations (LLMs, embeddings, recommendations)

This ADR will guide architectural decisions moving forward.
