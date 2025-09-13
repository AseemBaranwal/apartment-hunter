import pytest
from unittest.mock import AsyncMock, MagicMock

from ...app import crud, models


@pytest.mark.asyncio
async def test_get_communities_returns_result():
    community1 = models.Community(
        name="Alpha",
        street="123 First St",
        city="Springfield",
        lat=1.1,
        lon=2.2,
        primary_source="test",
    )
    community2 = models.Community(
        name="Beta",
        street="456 Second Ave",
        city="Shelbyville",
        lat=3.3,
        lon=4.4,
        primary_source="test",
    )
    scalars = MagicMock()
    scalars.unique.return_value.all.return_value = [community1, community2]

    result = MagicMock()
    result.scalars.return_value = scalars

    db = AsyncMock()
    db.execute.return_value = result

    communities = await crud.get_communities(db, skip=0, limit=10)

    db.execute.assert_awaited()
    assert communities == [community1, community2]
