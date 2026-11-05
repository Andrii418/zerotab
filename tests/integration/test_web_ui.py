import pytest

from tests.integration.helpers import create_person


def post_expense_form(client, seeded_group, **overrides):
    form = {
        "description": "Hotel",
        "category": "travel",
        "amount": "90,00",
        "payer_id": str(seeded_group.anna_id),
        "split_type": "equal",
        "participants": [
            str(seeded_group.anna_id),
            str(seeded_group.ben_id),
            str(seeded_group.carl_id),
        ],
    }
    form.update(overrides)
    return client.post(
        f"/ui/groups/{seeded_group.group_id}/expenses", data=form, follow_redirects=False
    )


def test_root_redirects_to_ui(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/ui"


def test_index_page_lists_existing_groups(client, seeded_group):
    # Arrange
    url = "/ui"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert "Your groups" in response.text
    assert "Trip" in response.text
    assert "3 members" in response.text


def test_create_person_form_adds_person_and_redirects(client):
    # Arrange
    form = {"name": "Dana"}

    # Act
    response = client.post("/ui/people", data=form, follow_redirects=False)

    # Assert
    assert response.status_code == 303
    assert response.headers["location"] == "/ui"
    assert [person["name"] for person in client.get("/people").json()] == ["Dana"]


def test_create_person_form_rejects_blank_name(client):
    # Arrange
    form = {"name": "   "}

    # Act
    response = client.post("/ui/people", data=form)

    # Assert
    assert response.status_code == 422
    assert "Name must not be blank" in response.text
    assert client.get("/people").json() == []


def test_create_group_form_redirects_to_new_group(client):
    # Arrange
    person_id = create_person(client, "Anna")
    form = {"name": "Weekend", "member_ids": [str(person_id)]}

    # Act
    response = client.post("/ui/groups", data=form, follow_redirects=False)

    # Assert
    assert response.status_code == 303
    assert response.headers["location"].startswith("/ui/groups/")


def test_create_group_form_rejects_blank_name(client):
    # Arrange
    person_id = create_person(client, "Anna")
    form = {"name": "   ", "member_ids": [str(person_id)]}

    # Act
    response = client.post("/ui/groups", data=form)

    # Assert
    assert response.status_code == 422
    assert "Group name must not be blank" in response.text


def test_group_page_shows_members_and_empty_expense_list(client, seeded_group):
    # Arrange
    url = f"/ui/groups/{seeded_group.group_id}"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert "Anna" in response.text and "Ben" in response.text and "Carl" in response.text
    assert "No expenses yet." in response.text
    assert "All settled up." in response.text


def test_group_page_returns_404_for_unknown_group(client):
    # Arrange
    url = "/ui/groups/999"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 404


def test_add_expense_form_redirects_and_page_shows_expense_balances_and_settlement(client, seeded_group):
    # Arrange
    group_url = f"/ui/groups/{seeded_group.group_id}"

    # Act
    response = post_expense_form(client, seeded_group)
    page = client.get(group_url)

    # Assert
    assert response.status_code == 303
    assert response.headers["location"] == group_url
    assert "Hotel" in page.text
    assert "90.00 PLN" in page.text
    assert "60.00 PLN" in page.text
    assert "-30.00 PLN" in page.text
    assert "pays" in page.text


def test_add_expense_form_accepts_percentage_split(client, seeded_group):
    # Arrange
    overrides = {
        "split_type": "percentage",
        "participants": [str(seeded_group.anna_id), str(seeded_group.ben_id)],
        f"share_{seeded_group.anna_id}": "70",
        f"share_{seeded_group.ben_id}": "30",
    }

    # Act
    response = post_expense_form(client, seeded_group, **overrides)

    # Assert
    shares = client.get(f"/groups/{seeded_group.group_id}/expenses").json()[0]["shares"]
    assert response.status_code == 303
    assert {share["person_id"]: share["amount"] for share in shares} == {
        seeded_group.anna_id: "63.00",
        seeded_group.ben_id: "27.00",
    }


def test_add_expense_form_shows_error_for_percentages_not_summing_to_hundred(client, seeded_group):
    # Arrange
    overrides = {
        "split_type": "percentage",
        "participants": [str(seeded_group.anna_id), str(seeded_group.ben_id)],
        f"share_{seeded_group.anna_id}": "60",
        f"share_{seeded_group.ben_id}": "30",
    }

    # Act
    response = post_expense_form(client, seeded_group, **overrides)

    # Assert
    assert response.status_code == 422
    assert "Percentages must sum to 100" in response.text
    assert client.get(f"/groups/{seeded_group.group_id}/expenses").json() == []


def test_add_expense_form_shows_error_for_exact_amounts_not_matching_total(client, seeded_group):
    # Arrange
    overrides = {
        "split_type": "exact",
        "participants": [str(seeded_group.anna_id), str(seeded_group.ben_id)],
        f"share_{seeded_group.anna_id}": "50",
        f"share_{seeded_group.ben_id}": "20",
    }

    # Act
    response = post_expense_form(client, seeded_group, **overrides)

    # Assert
    assert response.status_code == 422
    assert "Amounts must sum to the total" in response.text


@pytest.mark.parametrize("amount", ["abc", "NaN", ""])
def test_add_expense_form_shows_error_for_invalid_amount(client, seeded_group, amount):
    # Arrange
    overrides = {"amount": amount}

    # Act
    response = post_expense_form(client, seeded_group, **overrides)

    # Assert
    assert response.status_code == 422
    assert client.get(f"/groups/{seeded_group.group_id}/expenses").json() == []


def test_delete_expense_form_removes_expense(client, seeded_group):
    # Arrange
    post_expense_form(client, seeded_group)
    expense_id = client.get(f"/groups/{seeded_group.group_id}/expenses").json()[0]["id"]

    # Act
    response = client.post(
        f"/ui/groups/{seeded_group.group_id}/expenses/{expense_id}/delete",
        follow_redirects=False,
    )

    # Assert
    assert response.status_code == 303
    assert client.get(f"/groups/{seeded_group.group_id}/expenses").json() == []


def test_add_member_form_adds_person_to_group(client, seeded_group):
    # Arrange
    dave_id = create_person(client, "Dave")

    # Act
    response = client.post(
        f"/ui/groups/{seeded_group.group_id}/members",
        data={"person_id": str(dave_id)},
        follow_redirects=False,
    )

    # Assert
    members = client.get(f"/groups/{seeded_group.group_id}").json()["members"]
    assert response.status_code == 303
    assert len(members) == 4


def test_delete_group_form_removes_group(client, seeded_group):
    # Arrange
    url = f"/ui/groups/{seeded_group.group_id}/delete"

    # Act
    response = client.post(url, follow_redirects=False)

    # Assert
    assert response.status_code == 303
    assert response.headers["location"] == "/ui"
    assert client.get(f"/groups/{seeded_group.group_id}").status_code == 404

def test_add_member_form_returns_404_for_unknown_group(client):
    # Arrange
    dave_id = create_person(client, "Dave")

    # Act
    response = client.post("/ui/groups/999/members", data={"person_id": str(dave_id)})

    # Assert
    assert response.status_code == 404