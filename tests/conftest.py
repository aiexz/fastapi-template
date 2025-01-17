import pytest
from fastapi.testclient import TestClient

import app.dependancies as deps
from app.__main__ import app


class Database:
    def __init__(self, *args, **kwargs):
        pass

    async def ping(self) -> bool:
        return True


@pytest.fixture
def client():
    app.dependency_overrides[deps.DatabaseDependency] = lambda: Database("")
    return TestClient(app)
