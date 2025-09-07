from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models


async def get_communities(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Community)
        .options(
            selectinload(models.Community.listings)
            .selectinload(models.Listing.price_snapshots)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().unique().all()
