from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import communities
from .database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: nothing to clean up currently


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(communities.router)
