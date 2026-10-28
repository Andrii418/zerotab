from app.exceptions import EntityNotFoundError, InvalidExpenseError
from app.models import ExpenseGroup
from app.repositories.group_repository import GroupRepository
from app.repositories.person_repository import PersonRepository


class GroupService:
    def __init__(self, group_repository: GroupRepository, person_repository: PersonRepository) -> None:
        self._groups = group_repository
        self._people = person_repository

    def create_group(self, name: str, member_ids: list[int]) -> ExpenseGroup:
        if not name.strip():
            raise InvalidExpenseError("Group name must not be blank")
        members = [self._get_person(person_id) for person_id in set(member_ids)]
        return self._groups.add(name.strip(), members)

    def add_member(self, group_id: int, person_id: int) -> ExpenseGroup:
        group = self.get_group(group_id)
        self._groups.add_member(group, self._get_person(person_id))
        return group

    def get_group(self, group_id: int) -> ExpenseGroup:
        group = self._groups.get(group_id)
        if group is None:
            raise EntityNotFoundError(f"Group {group_id} not found")
        return group

    def list_groups(self) -> list[ExpenseGroup]:
        return self._groups.list_all()

    def delete_group(self, group_id: int) -> None:
        self._groups.delete(self.get_group(group_id))

    def _get_person(self, person_id: int):
        person = self._people.get(person_id)
        if person is None:
            raise EntityNotFoundError(f"Person {person_id} not found")
        return person