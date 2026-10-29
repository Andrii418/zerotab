from fastapi import APIRouter, status

from app.dependencies import GroupServiceDep
from app.models import ExpenseGroup
from app.schemas.group import GroupCreate, GroupRead, MemberAdd

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(payload: GroupCreate, service: GroupServiceDep) -> ExpenseGroup:
    return service.create_group(payload.name, payload.member_ids)


@router.get("", response_model=list[GroupRead])
def list_groups(service: GroupServiceDep) -> list[ExpenseGroup]:
    return service.list_groups()


@router.get("/{group_id}", response_model=GroupRead)
def get_group(group_id: int, service: GroupServiceDep) -> ExpenseGroup:
    return service.get_group(group_id)


@router.post("/{group_id}/members", response_model=GroupRead)
def add_member(group_id: int, payload: MemberAdd, service: GroupServiceDep) -> ExpenseGroup:
    return service.add_member(group_id, payload.person_id)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, service: GroupServiceDep) -> None:
    service.delete_group(group_id)