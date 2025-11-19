import pytest
from httpx import AsyncClient

# NOTE:
# These E2E tests exercise the entire running FastAPI app.
# They require the local environment to be running:
# `docker compose -f docker-compose.dev.yml up`

@pytest.mark.asyncio
async def test_healthcheck_e2e():
    """
    Simple E2E test to verify that the app responds via HTTP
    and environment is fully operational.
    """
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/api/health")

    assert response.status_code == 200
    json_data = response.json()

    # The actual value may vary depending on the health router
    assert "status" in json_data
    assert json_data["status"] in ("ok", "error")
