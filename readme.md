# FastAPI Template

## Stack
- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL
 - OpenTelemetry (traces & metrics)
 - VictoriaMetrics (OTLP metrics receiver)
 - Grafana Tempo (OTLP traces)
 - Grafana (dashboarding / datasource provisioning)

## Usage
```bash
uv venv
uv sync
uv run uvicorn app.__main__:app --reload
```

Telemetry
---------

This template includes basic OpenTelemetry:
- A TracerProvider that exports *traces*
- A MeterProvider that exports *metrics*
- Instrumentation for FastAPI and SQLAlchemy


## Docker
```bash
docker build -t fastapi-template .
docker run -p 8000:8000 fastapi-template
```
There is also 

Dev compose
-------------------
There is a dev compose file that includes the database, telemetry backends, and Grafana(with a pre-configured datasource):

```bash
docker compose -f docker-compose.dev.yml up --build
```