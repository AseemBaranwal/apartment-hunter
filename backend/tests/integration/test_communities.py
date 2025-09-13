import pytest
import pytest_asyncio
from pytest import mark
from httpx import AsyncClient, ASGITransport

from ...app.main import app
from ...app import models, crud, database
from uuid import uuid4
from datetime import datetime


@pytest_asyncio.fixture
async def client(monkeypatch):
    async def override_get_db():
        yield None

    app.dependency_overrides[database.get_db] = override_get_db

    community = models.Community(
        id=uuid4(),
        name="Test",
        primary_source="test",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    async def mock_get_communities(db, skip=0, limit=10):
        return [community]

    monkeypatch.setattr(crud, "get_communities", mock_get_communities)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@mark.asyncio
async def test_read_communities(client):
    resp = await client.get("/communities")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test"
