from typing import Annotated

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.dependencies import (
    ExpenseServiceDep,
    GroupPageDep,
    GroupServiceDep,
    PersonRepositoryDep,
)
from app.exceptions import (
    EntityNotFoundError,
    InvalidBalancesError,
    InvalidExpenseError,
    InvalidSplitError,
)
from app.repositories.person_repository import PersonRepository
from app.services.group_service import GroupService
from app.web.form_parser import parse_expense_form
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
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT if error else status.HTTP_200_OK
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


@router.get("/groups/{group_id}", response_class=HTMLResponse)
def group_detail(request: Request, group_id: int, page: GroupPageDep) -> HTMLResponse:
    return page.render(request, group_id)


@router.post("/groups/{group_id}/members")
def add_member(
    request: Request,
    group_id: int,
    person_id: Annotated[int, Form()],
    groups: GroupServiceDep,
    page: GroupPageDep,
) -> Response:
    try:
        groups.add_member(group_id, person_id)
    except DOMAIN_ERRORS as error:
        return page.render(request, group_id, error=str(error))
    return redirect(f"/ui/groups/{group_id}")


@router.post("/groups/{group_id}/expenses")
async def add_expense(
    request: Request,
    group_id: int,
    expenses: ExpenseServiceDep,
    page: GroupPageDep,
) -> Response:
    form = await request.form()
    try:
        expenses.add_expense(group_id=group_id, **parse_expense_form(form))
    except DOMAIN_ERRORS as error:
        return page.render(request, group_id, error=str(error))
    return redirect(f"/ui/groups/{group_id}")


@router.post("/groups/{group_id}/expenses/{expense_id}/delete")
def delete_expense(group_id: int, expense_id: int, expenses: ExpenseServiceDep) -> Response:
    expenses.delete_expense(expense_id)
    return redirect(f"/ui/groups/{group_id}")


@router.post("/groups/{group_id}/delete")
def delete_group(group_id: int, groups: GroupServiceDep) -> Response:
    groups.delete_group(group_id)
    return redirect("/ui")