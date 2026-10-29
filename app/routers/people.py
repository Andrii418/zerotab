from fastapi import APIRouter, status

from app.dependencies import PersonRepositoryDep
from app.models import Person
from app.schemas.person import PersonCreate, PersonRead

router = APIRouter(prefix="/people", tags=["people"])


@router.post("", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(payload: PersonCreate, people: PersonRepositoryDep) -> Person:
    return people.add(payload.name)


@router.get("", response_model=list[PersonRead])
def list_people(people: PersonRepositoryDep) -> list[Person]:
    return people.list_all()