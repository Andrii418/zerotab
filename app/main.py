from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import init_database
from app.error_handlers import register_error_handlers
from app.routers import expenses, groups, people, settlement, web
from app.web.templating import STATIC_DIR


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_database()
    yield


app = FastAPI(title="ZeroTab", lifespan=lifespan)
register_error_handlers(app)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(people.router)
app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(settlement.router)
app.include_router(web.router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/ui")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}