from unittest.mock import MagicMock

import pytest

from app.exceptions import EntityNotFoundError, InvalidExpenseError
from app.models import Person
from app.repositories.group_repository import GroupRepository
from app.repositories.person_repository import PersonRepository
from app.services.group_service import GroupService
from tests.builders import build_group


@pytest.fixture
def group_repository():
    return MagicMock(spec=GroupRepository)


@pytest.fixture
def person_repository():
    repository = MagicMock(spec=PersonRepository)
    repository.get.side_effect = lambda person_id: Person(id=person_id, name=f"Person {person_id}")
    return repository


@pytest.fixture
def service(group_repository, person_repository):
    return GroupService(group_repository, person_repository)


def test_create_group_saves_trimmed_name_with_loaded_members(service, group_repository):
    # Arrange
    name = "  Trip  "

    # Act
    service.create_group(name, [1, 2])

    # Assert
    saved_name, saved_members = group_repository.add.call_args.args
    assert saved_name == "Trip"
    assert {member.id for member in saved_members} == {1, 2}


def test_create_group_returns_group_created_by_repository(service, group_repository):
    # Arrange
    created_group = build_group()
    group_repository.add.return_value = created_group

    # Act
    result = service.create_group("Trip", [1])

    # Assert
    assert result is created_group


def test_create_group_ignores_duplicate_member_ids(service, group_repository):
    # Arrange
    member_ids = [1, 1, 2, 2]

    # Act
    service.create_group("Trip", member_ids)

    # Assert
    _, saved_members = group_repository.add.call_args.args
    assert len(saved_members) == 2


@pytest.mark.parametrize("name", ["", "   "])
def test_create_group_rejects_blank_name(service, group_repository, name):
    # Arrange
    blank_name = name

    # Act
    action = lambda: service.create_group(blank_name, [1])

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()
    group_repository.add.assert_not_called()


def test_create_group_rejects_unknown_member(service, person_repository, group_repository):
    # Arrange
    person_repository.get.side_effect = lambda person_id: None

    # Act
    action = lambda: service.create_group("Trip", [99])

    # Assert
    with pytest.raises(EntityNotFoundError):
        action()
    group_repository.add.assert_not_called()


def test_get_group_returns_existing_group(service, group_repository):
    # Arrange
    stored_group = build_group()
    group_repository.get.return_value = stored_group

    # Act
    result = service.get_group(1)

    # Assert
    assert result is stored_group


def test_get_group_rejects_unknown_group(service, group_repository):
    # Arrange
    group_repository.get.return_value = None

    # Act
    action = lambda: service.get_group(1)

    # Assert
    with pytest.raises(EntityNotFoundError):
        action()


def test_add_member_passes_group_and_person_to_repository(service, group_repository):
    # Arrange
    stored_group = build_group()
    group_repository.get.return_value = stored_group

    # Act
    result = service.add_member(1, 4)

    # Assert
    added_group, added_person = group_repository.add_member.call_args.args
    assert added_group is stored_group
    assert added_person.id == 4
    assert result is stored_group


def test_add_member_rejects_unknown_person(service, person_repository, group_repository):
    # Arrange
    group_repository.get.return_value = build_group()
    person_repository.get.side_effect = lambda person_id: None

    # Act
    action = lambda: service.add_member(1, 99)

    # Assert
    with pytest.raises(EntityNotFoundError):
        action()
    group_repository.add_member.assert_not_called()


def test_list_groups_returns_groups_from_repository(service, group_repository):
    # Arrange
    stored_groups = [build_group(1), build_group(2)]
    group_repository.list_all.return_value = stored_groups

    # Act
    result = service.list_groups()

    # Assert
    assert result == stored_groups


def test_delete_group_removes_existing_group(service, group_repository):
    # Arrange
    stored_group = build_group()
    group_repository.get.return_value = stored_group

    # Act
    service.delete_group(1)

    # Assert
    group_repository.delete.assert_called_once_with(stored_group)


def test_delete_group_rejects_unknown_group(service, group_repository):
    # Arrange
    group_repository.get.return_value = None

    # Act
    action = lambda: service.delete_group(1)

    # Assert
    with pytest.raises(EntityNotFoundError):
        action()
    group_repository.delete.assert_not_called()