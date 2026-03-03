# Sheenly Backend

FastAPI backend with PostgreSQL for inventory management.

## Stack

- **Python** 3.12+
- **FastAPI** — REST API framework
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **PostgreSQL** — database
- **uv** — package manager

## Setup

1. Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
uv sync
```

3. Run database migrations:

```bash
uv run alembic upgrade head
```

## Running

```bash
uv run uvicorn main:app --reload
```

API docs available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

```bash
# Lint and auto-fix
uv run ruff check . --fix

# Format
uv run ruff format .

# Run tests
uv run pytest tests/

# Run tests with coverage
uv run pytest tests/ --cov=app
```
