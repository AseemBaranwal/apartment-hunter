from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, database, schemas

router = APIRouter()


@router.get("/communities", response_model=list[schemas.CommunityOut])
async def read_communities(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_communities(db, skip=skip, limit=limit)
