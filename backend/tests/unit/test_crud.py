import pytest
from unittest.mock import AsyncMock, MagicMock

from ...app import crud, models


@pytest.mark.asyncio
async def test_get_communities_returns_result():
    community = models.Community(name="Test", primary_source="test")
    scalars = MagicMock()
    scalars.unique.return_value.all.return_value = [community]

    result = MagicMock()
    result.scalars.return_value = scalars

    db = AsyncMock()
    db.execute.return_value = result

    communities = await crud.get_communities(db, skip=0, limit=10)

    db.execute.assert_awaited()
    assert communities == [community]
