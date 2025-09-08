from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, database, schemas

router = APIRouter()


@router.get("/communities", response_model=list[schemas.CommunityOut])
async def read_communities(
    db: Annotated[AsyncSession, Depends(database.get_db)],
    skip: int = 0,
    limit: int = 10,
):
    return await crud.get_communities(db, skip=skip, limit=limit)
