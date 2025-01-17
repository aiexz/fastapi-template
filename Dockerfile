FROM python:3.12-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.0.1

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

# if your project is stored in src, uncomment line below
# or this if your file is stored in $PROJECT_NAME, assuming `myproject`
#COPY myproject ./myproject
RUN poetry config virtualenvs.in-project true && \
    poetry lock

RUN poetry export --without-hashes -o requirements.txt && \
    poetry run python -m pip wheel --no-cache-dir --wheel-dir=/app/dist -r requirements.txt


FROM base AS final

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist /app/dist

RUN ./.venv/bin/pip install /app/dist/*.whl

COPY app ./app

CMD ["./.venv/bin/uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "80"]