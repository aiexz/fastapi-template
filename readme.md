# FastAPI Template

## Stack
- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL

## Usage
```bash
poetry install
poetry run uvicorn app.__main__:app --reload
```

## Tests
```bash
poetry install --with dev
poetry run pytest
```

## Docker
```bash
docker build -t fastapi-template .
docker run -p 8000:8000 fastapi-template
```