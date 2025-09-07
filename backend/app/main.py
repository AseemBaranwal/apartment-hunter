from fastapi import FastAPI
from .routers import communities
from .database import engine, Base

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(communities.router)
