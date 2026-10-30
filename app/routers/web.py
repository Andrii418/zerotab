from typing import Annotated

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.dependencies import GroupServiceDep, PersonRepositoryDep
from app.exceptions import (
    EntityNotFoundError,
    InvalidBalancesError,
    InvalidExpenseError,
    InvalidSplitError,
)
from app.repositories.person_repository import PersonRepository
from app.services.group_service import GroupService
from app.web.templating import templates

router = APIRouter(prefix="/ui", include_in_schema=False)

DOMAIN_ERRORS = (
    EntityNotFoundError,
    InvalidBalancesError,
    InvalidExpenseError,
    InvalidSplitError,
)


def redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


def render_index(
    request: Request,
    people: PersonRepository,
    groups: GroupService,
    error: str | None = None,
) -> HTMLResponse:
    context = {"people": people.list_all(), "groups": groups.list_groups(), "error": error}
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY if error else status.HTTP_200_OK
    return templates.TemplateResponse(request, "index.html", context, status_code=status_code)


@router.get("", response_class=HTMLResponse)
def index(request: Request, people: PersonRepositoryDep, groups: GroupServiceDep) -> HTMLResponse:
    return render_index(request, people, groups)


@router.post("/people")
def create_person(
    request: Request,
    name: Annotated[str, Form()],
    people: PersonRepositoryDep,
    groups: GroupServiceDep,
) -> Response:
    clean_name = name.strip()
    if not clean_name:
        return render_index(request, people, groups, error="Name must not be blank")
    people.add(clean_name)
    return redirect("/ui")


@router.post("/groups")
def create_group(
    request: Request,
    name: Annotated[str, Form()],
    people: PersonRepositoryDep,
    groups: GroupServiceDep,
    member_ids: Annotated[list[int] | None, Form()] = None,
) -> Response:
    try:
        group = groups.create_group(name, member_ids or [])
    except DOMAIN_ERRORS as error:
        return render_index(request, people, groups, error=str(error))
    return redirect(f"/ui/groups/{group.id}")