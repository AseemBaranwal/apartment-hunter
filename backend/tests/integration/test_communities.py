import pytest
import pytest_asyncio
from pytest import mark
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from ...app.main import app
from ...app import models, crud, database
from uuid import uuid4
from datetime import datetime


@pytest_asyncio.fixture
async def client():
    async def override_get_db():
        yield None

    app.dependency_overrides[database.get_db] = override_get_db

    community1 = models.Community(
        id=uuid4(),
        name="Alpha",
        street="123 First St",
        city="Springfield",
        lat=1.1,
        lon=2.2,
        primary_source="test",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    community2 = models.Community(
        id=uuid4(),
        name="Beta",
        street="456 Second Ave",
        city="Shelbyville",
        lat=3.3,
        lon=4.4,
        primary_source="test",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    async def mock_get_communities(db, skip=0, limit=10):
        return [community1, community2]

    with patch.object(crud, "get_communities", mock_get_communities):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()


@mark.asyncio
async def test_read_communities(client):
    resp = await client.get("/communities")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    expected = {
        ("Alpha", "123 First St", "Springfield", 1.1, 2.2),
        ("Beta", "456 Second Ave", "Shelbyville", 3.3, 4.4),
    }
    received = {
        (d["name"], d["street"], d["city"], d["lat"], d["lon"]) for d in data
    }
    assert received == expected
