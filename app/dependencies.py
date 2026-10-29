from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.person_repository import PersonRepository
from app.services.expense_service import ExpenseService
from app.services.group_service import GroupService
from app.services.settlement_service import SettlementService

SessionDep = Annotated[Session, Depends(get_session)]


def get_person_repository(session: SessionDep) -> PersonRepository:
    return PersonRepository(session)


def get_group_service(session: SessionDep) -> GroupService:
    return GroupService(GroupRepository(session), PersonRepository(session))


def get_expense_service(session: SessionDep) -> ExpenseService:
    return ExpenseService(ExpenseRepository(session), GroupRepository(session))


def get_settlement_service(session: SessionDep) -> SettlementService:
    return SettlementService(ExpenseRepository(session))


PersonRepositoryDep = Annotated[PersonRepository, Depends(get_person_repository)]
GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]
ExpenseServiceDep = Annotated[ExpenseService, Depends(get_expense_service)]
SettlementServiceDep = Annotated[SettlementService, Depends(get_settlement_service)]