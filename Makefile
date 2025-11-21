SHELL := /bin/bash

DC = docker compose -f docker-compose.dev.yml

# --- Containers ---
up:
	$(DC) up -d --build

down:
	$(DC) down

restart:
	$(DC) down && $(DC) up -d

logs:
	$(DC) logs -f app

# --- Linting ---
lint:
	$(DC) exec app ruff check src

lint-fix:
	$(DC) exec app ruff check src --fix

types:
	$(DC) exec app mypy src

# --- Tests ---
test:
	$(DC) exec app pytest --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing

# --- Alembic migrations ---
migrate:
	$(DC) exec alembic alembic upgrade head

revision:
	$(DC) exec alembic alembic revision --autogenerate -m "$(m)"

# --- Utils ---
shell:
	$(DC) exec app bash

ps:
	$(DC) ps

# --- Full cleanup ---
clean:
	$(DC) down -v
	docker system prune -af --volumes
