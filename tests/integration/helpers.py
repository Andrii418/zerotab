from fastapi.testclient import TestClient
from httpx import Response


def create_person(client: TestClient, name: str) -> int:
    return client.post("/people", json={"name": name}).json()["id"]


def create_group(client: TestClient, name: str, member_ids: list[int]) -> int:
    response = client.post("/groups", json={"name": name, "member_ids": member_ids})
    return response.json()["id"]


def equal_expense_payload(
    payer_id: int,
    participant_ids: list[int],
    amount: str = "90.00",
    description: str = "Hotel",
) -> dict:
    return {
        "payer_id": payer_id,
        "description": description,
        "category": "travel",
        "amount": amount,
        "split_type": "equal",
        "shares": {str(person_id): "1" for person_id in participant_ids},
    }


def post_expense(client: TestClient, group_id: int, payload: dict) -> Response:
    return client.post(f"/groups/{group_id}/expenses", json=payload)