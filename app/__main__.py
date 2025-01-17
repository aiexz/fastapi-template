import os

import fastapi

from app.database.methods import Database


def setup_routes(fastaApiApp: fastapi.FastAPI):
    import app.routes.health

    fastaApiApp.include_router(app.routes.health.router)


def setup_dependencies(fastaApiApp: fastapi.FastAPI):
    import app.dependancies

    database = Database(
            os.getenv(
                    "DATABASE_URL",
                    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
            ))
    fastaApiApp.dependency_overrides[app.dependancies.DatabaseDependency] = lambda: database()


app = fastapi.FastAPI()

setup_dependencies(app)

setup_routes(app)
