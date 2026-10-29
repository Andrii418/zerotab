from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_database
from app.error_handlers import register_error_handlers
from app.routers import expenses, groups, people, settlement


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_database()
    yield


app = FastAPI(title="ZeroTab", lifespan=lifespan)
register_error_handlers(app)
app.include_router(people.router)
app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(settlement.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}