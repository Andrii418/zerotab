import pytest

from tests.integration.helpers import (
    create_group,
    create_person,
    equal_expense_payload,
    post_expense,
)


def everyone(seeded_group) -> list[int]:
    return [seeded_group.anna_id, seeded_group.ben_id, seeded_group.carl_id]


def test_health_endpoint_returns_ok(client):
    # Arrange
    url = "/health"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_person_returns_created_person(client):
    # Arrange
    payload = {"name": "Anna"}

    # Act
    response = client.post("/people", json=payload)

    # Assert
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Anna"}


@pytest.mark.parametrize("name", ["", "   "])
def test_create_person_rejects_blank_name(client, name):
    # Arrange
    payload = {"name": name}

    # Act
    response = client.post("/people", json=payload)

    # Assert
    assert response.status_code == 422


def test_list_people_returns_people_sorted_by_name(client):
    # Arrange
    for name in ("Carl", "Anna", "Ben"):
        create_person(client, name)

    # Act
    response = client.get("/people")

    # Assert
    assert [person["name"] for person in response.json()] == ["Anna", "Ben", "Carl"]


def test_create_group_returns_group_with_members(client):
    # Arrange
    member_ids = [create_person(client, "Anna"), create_person(client, "Ben")]

    # Act
    response = client.post("/groups", json={"name": "Trip", "member_ids": member_ids})

    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "Trip"
    assert {member["id"] for member in response.json()["members"]} == set(member_ids)


def test_create_group_rejects_unknown_member(client):
    # Arrange
    payload = {"name": "Trip", "member_ids": [999]}

    # Act
    response = client.post("/groups", json=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Person 999 not found"


def test_get_group_returns_404_for_unknown_group(client):
    # Arrange
    unknown_group_id = 999

    # Act
    response = client.get(f"/groups/{unknown_group_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Group 999 not found"


def test_add_member_extends_group(client):
    # Arrange
    anna_id = create_person(client, "Anna")
    ben_id = create_person(client, "Ben")
    group_id = create_group(client, "Trip", [anna_id])

    # Act
    response = client.post(f"/groups/{group_id}/members", json={"person_id": ben_id})

    # Assert
    assert response.status_code == 200
    assert {member["id"] for member in response.json()["members"]} == {anna_id, ben_id}


def test_delete_group_removes_group(client, seeded_group):
    # Arrange
    group_id = seeded_group.group_id

    # Act
    delete_response = client.delete(f"/groups/{group_id}")
    get_response = client.get(f"/groups/{group_id}")

    # Assert
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_add_equal_expense_returns_cent_exact_shares(client, seeded_group):
    # Arrange
    payload = equal_expense_payload(seeded_group.anna_id, everyone(seeded_group), "100.00")

    # Act
    response = post_expense(client, seeded_group.group_id, payload)

    # Assert
    shares = {share["person_id"]: share["amount"] for share in response.json()["shares"]}
    assert response.status_code == 201
    assert response.json()["amount"] == "100.00"
    assert shares == {
        seeded_group.anna_id: "33.34",
        seeded_group.ben_id: "33.33",
        seeded_group.carl_id: "33.33",
    }


def test_add_percentage_expense_gives_leftover_cent_to_largest_remainder(client, seeded_group):
    # Arrange
    payload = {
        "payer_id": seeded_group.anna_id,
        "description": "Dinner",
        "amount": "100.01",
        "split_type": "percentage",
        "shares": {
            str(seeded_group.anna_id): "50",
            str(seeded_group.ben_id): "30",
            str(seeded_group.carl_id): "20",
        },
    }

    # Act
    response = post_expense(client, seeded_group.group_id, payload)

    # Assert
    shares = {share["person_id"]: share["amount"] for share in response.json()["shares"]}
    assert response.status_code == 201
    assert shares == {
        seeded_group.anna_id: "50.01",
        seeded_group.ben_id: "30.00",
        seeded_group.carl_id: "20.00",
    }


def test_add_exact_expense_stores_given_amounts(client, seeded_group):
    # Arrange
    payload = {
        "payer_id": seeded_group.anna_id,
        "description": "Tickets",
        "amount": "100.00",
        "split_type": "exact",
        "shares": {str(seeded_group.anna_id): "60.00", str(seeded_group.ben_id): "40.00"},
    }

    # Act
    response = post_expense(client, seeded_group.group_id, payload)

    # Assert
    shares = {share["person_id"]: share["amount"] for share in response.json()["shares"]}
    assert response.status_code == 201
    assert shares == {seeded_group.anna_id: "60.00", seeded_group.ben_id: "40.00"}


def test_add_expense_rejects_payer_outside_group(client, seeded_group):
    # Arrange
    outsider_id = create_person(client, "Dave")
    payload = equal_expense_payload(outsider_id, everyone(seeded_group))

    # Act
    response = post_expense(client, seeded_group.group_id, payload)

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"] == "Payer must be a member of the group"


@pytest.mark.parametrize("amount", ["0", "-5.00"])
def test_add_expense_rejects_non_positive_amount(client, seeded_group, amount):
    # Arrange
    payload = equal_expense_payload(seeded_group.anna_id, everyone(seeded_group), amount)

    # Act
    response = post_expense(client, seeded_group.group_id, payload)

    # Assert
    assert response.status_code == 422


def test_add_expense_rejects_percentages_not_summing_to_hundred(client, seeded_group):
    # Arrange
    payload = {
        "payer_id": seeded_group.anna_id,
        "description": "Dinner",
        "amount": "100.00",
        "split_type": "percentage",
        "shares": {str(seeded_group.anna_id): "60", str(seeded_group.ben_id): "30"},
    }

    # Act
    response = post_expense(client, seeded_group.group_id, payload)

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"] == "Percentages must sum to 100"


def test_add_expense_to_unknown_group_returns_404(client):
    # Arrange
    payload = equal_expense_payload(1, [1])

    # Act
    response = post_expense(client, 999, payload)

    # Assert
    assert response.status_code == 404


def test_list_expenses_returns_added_expenses(client, seeded_group):
    # Arrange
    participants = everyone(seeded_group)
    post_expense(client, seeded_group.group_id, equal_expense_payload(seeded_group.anna_id, participants))
    post_expense(
        client,
        seeded_group.group_id,
        equal_expense_payload(seeded_group.ben_id, participants, "30.00", "Taxi"),
    )

    # Act
    response = client.get(f"/groups/{seeded_group.group_id}/expenses")

    # Assert
    assert response.status_code == 200
    assert {expense["description"] for expense in response.json()} == {"Hotel", "Taxi"}


def test_delete_expense_removes_it_from_group(client, seeded_group):
    # Arrange
    payload = equal_expense_payload(seeded_group.anna_id, everyone(seeded_group))
    expense_id = post_expense(client, seeded_group.group_id, payload).json()["id"]

    # Act
    delete_response = client.delete(f"/expenses/{expense_id}")
    list_response = client.get(f"/groups/{seeded_group.group_id}/expenses")

    # Assert
    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_delete_unknown_expense_returns_404(client):
    # Arrange
    unknown_expense_id = 999

    # Act
    response = client.delete(f"/expenses/{unknown_expense_id}")

    # Assert
    assert response.status_code == 404


def test_balances_endpoint_returns_balance_per_person(client, seeded_group):
    # Arrange
    payload = equal_expense_payload(seeded_group.anna_id, everyone(seeded_group))
    post_expense(client, seeded_group.group_id, payload)

    # Act
    response = client.get(f"/groups/{seeded_group.group_id}/balances")

    # Assert
    balances = {row["person_id"]: row["amount"] for row in response.json()}
    assert balances == {
        seeded_group.anna_id: "60.00",
        seeded_group.ben_id: "-30.00",
        seeded_group.carl_id: "-30.00",
    }


def test_balances_return_to_empty_after_expense_is_deleted(client, seeded_group):
    # Arrange
    payload = equal_expense_payload(seeded_group.anna_id, everyone(seeded_group))
    expense_id = post_expense(client, seeded_group.group_id, payload).json()["id"]
    client.delete(f"/expenses/{expense_id}")

    # Act
    response = client.get(f"/groups/{seeded_group.group_id}/balances")

    # Assert
    assert response.json() == []


def test_settlement_endpoint_returns_minimal_transfers(client, seeded_group):
    # Arrange
    participants = everyone(seeded_group)
    post_expense(client, seeded_group.group_id, equal_expense_payload(seeded_group.anna_id, participants))
    post_expense(
        client,
        seeded_group.group_id,
        equal_expense_payload(seeded_group.ben_id, participants, "30.00", "Taxi"),
    )

    # Act
    response = client.get(f"/groups/{seeded_group.group_id}/settlement")

    # Assert
    transfers = {(row["payer_id"], row["receiver_id"], row["amount"]) for row in response.json()}
    assert transfers == {
        (seeded_group.carl_id, seeded_group.anna_id, "40.00"),
        (seeded_group.ben_id, seeded_group.anna_id, "10.00"),
    }


def test_settlement_endpoint_returns_empty_list_without_expenses(client, seeded_group):
    # Arrange
    group_id = seeded_group.group_id

    # Act
    response = client.get(f"/groups/{group_id}/settlement")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_settlement_endpoint_returns_404_for_unknown_group(client):
    # Arrange
    unknown_group_id = 999

    # Act
    response = client.get(f"/groups/{unknown_group_id}/settlement")

    # Assert
    assert response.status_code == 404