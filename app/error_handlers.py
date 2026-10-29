from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    EntityNotFoundError,
    InvalidBalancesError,
    InvalidExpenseError,
    InvalidSplitError,
)


def _json_error(status_code: int, error: Exception) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": str(error)})


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundError)
    async def handle_not_found(_: Request, error: EntityNotFoundError) -> JSONResponse:
        return _json_error(status.HTTP_404_NOT_FOUND, error)

    @app.exception_handler(InvalidSplitError)
    @app.exception_handler(InvalidExpenseError)
    @app.exception_handler(InvalidBalancesError)
    async def handle_invalid_input(_: Request, error: Exception) -> JSONResponse:
        return _json_error(status.HTTP_422_UNPROCESSABLE_ENTITY, error)