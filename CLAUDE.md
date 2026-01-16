# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack web application for havrilesko.com with a React frontend and FastAPI backend, using Lando for local development.

## Development Commands

### Frontend (from `frontend/` directory)
```bash
pnpm dev        # Start Vite dev server (port 3000)
pnpm build      # TypeScript check + Vite build
pnpm lint       # ESLint check
```

### Backend (via Lando, from project root)
```bash
lando python-test     # Run pytest with parallel execution
lando python-lint     # black + isort + flake8 checks
lando python-lint:fix # Auto-format Python code
lando migrate         # Run Alembic migrations
lando makemigrations  # Create new migration
lando runserver       # Start FastAPI dev server (port 8000)
```

### Database
```bash
lando psql            # Access PostgreSQL CLI
```

## Architecture

### Tech Stack
- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS 4 + React Router 7 + TanStack Query
- **Backend**: FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL 17 + Python 3.12
- **Infrastructure**: Lando (Docker-based local dev)

### Backend Structure (`backend/app/`)
- `api/v1/` - Route handlers (auth.py, users.py) with `router.py` aggregating all routes
- `api/deps.py` - JWT dependencies and `get_current_user` injection
- `core/` - Config, database, security, exceptions
- `models/` - SQLAlchemy models
- `schemas/` - Pydantic request/response schemas
- `services/` - Business logic layer (auth_service.py, user_service.py)

### Frontend Structure (`frontend/src/`)
- `pages/` - Page components
- `components/` - Reusable components including `ui/` for base components
- `constants/` - Router setup and route definitions
- `lib/utils.ts` - `cn()` utility for className merging
- Path alias: `@/*` maps to `src/*`

### Authentication
- RS256 JWT signing with per-user token key for invalidation
- Access tokens: 5-minute TTL
- Refresh tokens: 30-day TTL
- Token key rotation on logout allows per-user session invalidation without blacklist

## Code Style

### Python
- Black formatter (90 char line length)
- isort for import sorting
- flake8 for linting
- mypy for type checking
- Config in `pyproject.toml`

### TypeScript
- Prettier (80 char, semicolons, double quotes)
- ESLint with TypeScript and React hooks plugins
- Strict mode with noUnusedLocals/noUnusedParameters

## Testing

Backend tests use pytest with:
- pytest-xdist for parallel execution
- In-memory SQLite for test database
- Fixtures in `backend/tests/conftest.py`

Run a single test:
```bash
lando ssh -c "cd /app && python -m pytest tests/api/v1/test_auth.py::test_name -v"
```
