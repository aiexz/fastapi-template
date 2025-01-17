import pytest


@pytest.mark.asyncio
async def test_ping(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"alive": True, "version": "0.1.0"}
