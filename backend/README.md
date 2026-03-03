uv run uvicorn main:app --reload

# Check and auto-fix

uv run --directory backend ruff check . --fix
uv run --directory backend ruff format .
