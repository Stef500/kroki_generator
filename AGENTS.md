# Repository Guidelines

## Project Structure & Modules
- `src/`: Flask app code (`main.py`, `routes.py`, `kroki_client.py`, `config.py`)
- `tests/`: Pytest suite (unit + `@pytest.mark.integration`)
- `templates/`, `static/`: UI assets
- `scripts/`: utility scripts
- `deploy/`: install and compose assets
- Config: `.env.template` → copy to `.env`

## Build, Test, Run
- Install dev deps: `make install` (uses `uv` for `.[test,dev]`)
- Run app (Flask only): `make run` (expects external Kroki)
- Full dev stack: `make dev` (starts Kroki services via Docker, then Flask)
- Tests + coverage: `make test`
- Lint checks: `make lint` (Black check + Ruff)
- Auto-format: `make format`
- Docker workflow: `make docker`, `make docker-build`, `make docker-stop`

## Coding Style & Conventions
- Language: Python 3.12+
- Formatting: Black (line length 88). Run `make format`.
- Linting: Ruff. Keep imports tidy and fix warnings.
- Indentation: 4 spaces; avoid trailing whitespace.
- Naming: modules `snake_case.py`; classes `PascalCase`; functions/vars `snake_case`.
- Module layout: keep HTTP logic in `routes.py`, Kroki API in `kroki_client.py`, config in `config.py`.

## Testing Guidelines
- Framework: Pytest with `pytest-cov`.
- Conventions: files `tests/test_*.py`; classes `Test*`; functions `test_*`.
- Integration tests: mark with `@pytest.mark.integration`; run via `pytest -m integration`.
- Coverage: pre-commit enforces `--cov-fail-under=80`. Aim ≥85%.
- Run locally: `make test` or `uv run pytest -v --cov=src`.

## Commit & Pull Requests
- Commits: short, imperative subject; use prefixes like `fix:`, `feat:`, `docs:`, `chore:` when clear (history often uses `fix ...`). Keep related changes together.
- PRs: include description, rationale, before/after notes, linked issues, and screenshots for UI changes. Ensure: `make test`, `make lint`, and `make format` pass.

## Security & Config
- Never commit secrets. Use `.env` (based on `.env.template`).
- Key vars: `KROKI_URL`, `REQUEST_TIMEOUT`, `MAX_BYTES`, `SECRET_KEY`, `FLASK_CONFIG`, `FLASK_PORT`.
- Validate diagram payload sizes and types before sending to Kroki.

## Agent Notes
- Prefer `Makefile` targets and `uv` to run tools.
- Keep changes minimal and aligned with the existing layout.
