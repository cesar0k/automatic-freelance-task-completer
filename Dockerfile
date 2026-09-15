FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/workspace/.venv/bin:$PATH"

WORKDIR /workspace

# Copy dependency manifests first for better layer caching.
# Root manifest + lock + every workspace member manifest.
COPY pyproject.toml uv.lock .python-version README.md ./
COPY packages/ packages/
COPY services/ services/

RUN uv sync --frozen --no-dev

# Default command is overridden per-service in docker-compose.yml,
# e.g.: uv run python -m services.tg_bot.main
CMD ["uv", "run", "python", "-m", "services.tg_bot.main"]
