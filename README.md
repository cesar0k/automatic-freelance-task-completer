# AI Freelance Order Pipeline

End-to-end freelance order automation system. Automatically scrapes new orders, orchestrates them through the pipeline, executes tasks using an AI coding agent, and sends real-time status updates via Telegram.

## Stack

Python 3.13 · `uv` · Docker Compose · PostgreSQL + SQLAlchemy 2 (async) · Redis ·
aiogram 3 · loguru · ruff

## Layout

```text
├── Dockerfile            # One image for all Python services (python:3.13-slim + uv)
├── docker-compose.yml    # Infra + services. No Makefile, compose is the interface.
├── .env.example          # Copy to .env to start.
├── pyproject.toml        # Single project file (deps + ruff). No per-service manifests.
├── services/             # Runnable apps: tg_bot, scraper, orchestrator, agent_runner
├── packages/             # Shared code: database, schemas (import as packages.database, ...)
├── skills/               # Reserved for agent prompts (empty for now)
└── storage/tasks/        # Where the agent writes code. Git-ignored, only .gitkeep is kept.
```

Services start as modules, e.g. `python -m services.tg_bot.main` — the same command runs
locally and inside Docker (compose uses `uv run --no-dev` so containers don't pull dev tools).

## Prerequisites

- Docker + Docker Compose v2
- Python 3.13
- `uv` ([install](https://docs.astral.sh/uv/getting-started/installation/))

Works on macOS (Docker Desktop) and Linux. On a Mac, keep heavy work inside containers —
bind mounts are slower there than on Linux.

## Setup

```bash
git clone https://github.com/cesar0k/automatic-freelance-task-completer.git
cd automatic-freelance-task-completer
cp .env.example .env   # then set POSTGRES_PASSWORD and BOT_TOKEN
uv sync                # install everything into .venv
docker compose up -d postgres redis
```

## Running services

Via Docker (same environment for everyone):

```bash
docker compose up --build tg_bot      # or scraper / orchestrator / agent_runner
docker compose up --build -d          # everything in the background
docker compose logs -f <service_name>
docker compose down
```

Locally (faster loop, infra still in Docker):

```bash
uv run python -m services.tg_bot.main
uv run python -m services.scraper.main
```

Tip: when running locally, set `DB_HOST=localhost` and `REDIS_HOST=localhost` in `.env`
— inside Compose they must stay `postgres` / `redis`.

## Code quality

One-time setup (after cloning, so checks run automatically on every commit):

```bash
uv sync
uv run pre-commit install
```

This installs git hooks: ruff lint + format and basic hygiene checks run on `git commit`
and fix/block bad code before it lands. The hook environments download once on first run,
then are reused.

Manual runs (same as what the hooks do):

```bash
uv run ruff check --fix .   # lint
uv run ruff format .        # format
uv run pre-commit run --all-files   # all hooks across the repo
```

If a hook modifies your files (e.g. fixes formatting), just `git add` the result and
commit again.

Generated agent code in `storage/tasks/` is excluded from git, ruff and pre-commit, so it
never pollutes diffs. Keep PRs small, one change each. Branch names:
`feature/...`, `fix/...`, `chore/...` — `main` is protected, no direct commits.
