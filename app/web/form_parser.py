from decimal import Decimal, InvalidOperation
from typing import Any

from starlette.datastructures import FormData

from app.exceptions import InvalidExpenseError, InvalidSplitError
from app.strategies.factory import SplitType

PARTICIPANTS_FIELD = "participants"
SHARE_FIELD_PREFIX = "share_"


def parse_decimal(raw_value: object) -> Decimal:
    try:
        value = Decimal(str(raw_value).strip().replace(",", "."))
    except InvalidOperation as error:
        raise InvalidSplitError("Enter a valid number") from error
    if not value.is_finite():
        raise InvalidSplitError("Enter a valid number")
    return value


def parse_shares(form: FormData, split_type: SplitType) -> dict[int, Decimal]:
    participant_ids = [int(str(value)) for value in form.getlist(PARTICIPANTS_FIELD)]
    if split_type is SplitType.EQUAL:
        return {participant_id: Decimal(1) for participant_id in participant_ids}
    return {
        participant_id: parse_decimal(form.get(f"{SHARE_FIELD_PREFIX}{participant_id}"))
        for participant_id in participant_ids
    }


def parse_expense_form(form: FormData) -> dict[str, Any]:
    try:
        split_type = SplitType(str(form["split_type"]))
        return {
            "payer_id": int(str(form["payer_id"])),
            "description": str(form["description"]),
            "category": str(form.get("category") or "other"),
            "amount": parse_decimal(form["amount"]),
            "split_type": split_type,
            "shares": parse_shares(form, split_type),
        }
    except InvalidSplitError:
        raise
    except (KeyError, ValueError) as error:
        raise InvalidExpenseError("Invalid expense form data") from error