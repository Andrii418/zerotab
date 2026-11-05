from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select

from app.models import Expense, ExpenseShare
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.person_repository import PersonRepository


def create_group_with_members(session, group_name="Trip"):
    people = PersonRepository(session)
    members = [people.add("Anna"), people.add("Ben")]
    return GroupRepository(session).add(group_name, members), members


def build_stored_expense(group_id, payer_id, description, created_at):
    return Expense(
        group_id=group_id,
        payer_id=payer_id,
        description=description,
        amount_cents=1000,
        created_at=created_at,
        shares=[ExpenseShare(person_id=payer_id, amount_cents=1000)],
    )


def test_person_repository_assigns_id_to_added_person(session):
    # Arrange
    repository = PersonRepository(session)

    # Act
    person = repository.add("Anna")

    # Assert
    assert person.id is not None
    assert repository.get(person.id).name == "Anna"


def test_person_repository_returns_none_for_unknown_person(session):
    # Arrange
    repository = PersonRepository(session)

    # Act
    person = repository.get(999)

    # Assert
    assert person is None


def test_person_repository_lists_people_ordered_by_name(session):
    # Arrange
    repository = PersonRepository(session)
    for name in ("Carl", "Anna", "Ben"):
        repository.add(name)

    # Act
    names = [person.name for person in repository.list_all()]

    # Assert
    assert names == ["Anna", "Ben", "Carl"]


def test_group_repository_persists_group_with_members(session):
    # Arrange
    group, members = create_group_with_members(session)

    # Act
    stored_group = GroupRepository(session).get(group.id)

    # Assert
    assert stored_group.name == "Trip"
    assert {member.id for member in stored_group.members} == {member.id for member in members}


def test_group_repository_does_not_add_member_twice(session):
    # Arrange
    group, members = create_group_with_members(session)
    repository = GroupRepository(session)

    # Act
    repository.add_member(group, members[0])

    # Assert
    assert len(repository.get(group.id).members) == 2


def test_group_repository_lists_groups_ordered_by_name(session):
    # Arrange
    create_group_with_members(session, "Weekend")
    create_group_with_members(session, "Birthday")

    # Act
    names = [group.name for group in GroupRepository(session).list_all()]

    # Assert
    assert names == ["Birthday", "Weekend"]


def test_group_repository_delete_cascades_to_expenses_and_shares(session):
    # Arrange
    group, members = create_group_with_members(session)
    expense = build_stored_expense(group.id, members[0].id, "Hotel", datetime.now(UTC))
    ExpenseRepository(session).add(expense)

    # Act
    GroupRepository(session).delete(group)

    # Assert
    assert session.get(Expense, expense.id) is None
    assert session.scalars(select(ExpenseShare)).all() == []


def test_expense_repository_lists_newest_expenses_first(session):
    # Arrange
    group, members = create_group_with_members(session)
    repository = ExpenseRepository(session)
    repository.add(build_stored_expense(group.id, members[0].id, "Old", datetime(2026, 1, 1)))
    repository.add(build_stored_expense(group.id, members[0].id, "New", datetime(2026, 2, 1)))

    # Act
    descriptions = [expense.description for expense in repository.list_by_group(group.id)]

    # Assert
    assert descriptions == ["New", "Old"]


def test_expense_repository_lists_only_expenses_of_requested_group(session):
    # Arrange
    group, members = create_group_with_members(session)
    other_group = GroupRepository(session).add("Other", members)
    repository = ExpenseRepository(session)
    repository.add(build_stored_expense(group.id, members[0].id, "Hotel", datetime.now(UTC)))
    repository.add(build_stored_expense(other_group.id, members[0].id, "Taxi", datetime.now(UTC)))

    # Act
    descriptions = [expense.description for expense in repository.list_by_group(group.id)]

    # Assert
    assert descriptions == ["Hotel"]


def test_expense_repository_delete_removes_expense_and_its_shares(session):
    # Arrange
    group, members = create_group_with_members(session)
    repository = ExpenseRepository(session)
    expense = repository.add(build_stored_expense(group.id, members[0].id, "Hotel", datetime.now(UTC)))

    # Act
    repository.delete(expense)

    # Assert
    assert repository.get(expense.id) is None
    assert session.scalars(select(ExpenseShare)).all() == []


def test_expense_and_share_expose_amount_as_decimal(session):
    # Arrange
    group, members = create_group_with_members(session)
    expense = ExpenseRepository(session).add(
        build_stored_expense(group.id, members[0].id, "Hotel", datetime.now(UTC))
    )

    # Act
    amounts = (expense.amount, expense.shares[0].amount)

    # Assert
    assert amounts == (Decimal("10.00"), Decimal("10.00"))