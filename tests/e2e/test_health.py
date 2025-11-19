import pytest


@pytest.mark.e2e
async def test_health_endpoint(client):
    """
    End-to-end test hitting the running FastAPI service.
    Ensures that:
    - The /api/health endpoint responds
    - The HTTP status is 200
    - The payload has the correct structure
    """
    response = await client.get("/api/health")

    assert response.status_code == 200, "Health endpoint did not return 200 OK"

    data = response.json()

    assert "status" in data
    assert data["status"] in ("ok", "healthy", "up")

    # optional: verify structure if your health response contains db status
    if "database" in data:
        assert data["database"] in ("ok", "healthy", "up")
