from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Person


class PersonRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, name: str) -> Person:
        person = Person(name=name)
        self._session.add(person)
        self._session.commit()
        return person

    def get(self, person_id: int) -> Person | None:
        return self._session.get(Person, person_id)

    def list_all(self) -> list[Person]:
        return list(self._session.scalars(select(Person).order_by(Person.name)))