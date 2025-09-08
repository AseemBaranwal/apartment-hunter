from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from collections.abc import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/apartmentdb"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
