FROM python:3.13-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
COPY --from=ghcr.io/astral-sh/uv:0.7.16 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv pip install --system -e .


FROM base AS final

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app ./app

EXPOSE 80

CMD ["/usr/local/bin/uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "80"]