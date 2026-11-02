from decimal import Decimal

import pytest
from starlette.datastructures import FormData

from app.exceptions import InvalidExpenseError, InvalidSplitError
from app.strategies.factory import SplitType
from app.web.form_parser import parse_decimal, parse_expense_form


def build_form(**fields: str) -> FormData:
    return FormData(list(fields.items()))


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [("12,50", Decimal("12.50")), (" 7 ", Decimal(7)), ("0.99", Decimal("0.99"))],
)
def test_parse_decimal_accepts_comma_and_whitespace(raw_value, expected):
    # Arrange
    value = raw_value

    # Act
    result = parse_decimal(value)

    # Assert
    assert result == expected


@pytest.mark.parametrize("raw_value", ["abc", "", "NaN", "Infinity"])
def test_parse_decimal_rejects_invalid_numbers(raw_value):
    # Arrange
    value = raw_value

    # Act
    action = lambda: parse_decimal(value)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()


def test_parse_expense_form_builds_equal_split_for_selected_participants():
    # Arrange
    form = FormData(
        [
            ("payer_id", "1"),
            ("description", "Hotel"),
            ("category", "travel"),
            ("amount", "90,50"),
            ("split_type", "equal"),
            ("participants", "1"),
            ("participants", "2"),
        ]
    )

    # Act
    result = parse_expense_form(form)

    # Assert
    assert result["amount"] == Decimal("90.50")
    assert result["split_type"] is SplitType.EQUAL
    assert result["shares"] == {1: Decimal(1), 2: Decimal(1)}


def test_parse_expense_form_reads_percentage_shares():
    # Arrange
    form = FormData(
        [
            ("payer_id", "1"),
            ("description", "Dinner"),
            ("amount", "100"),
            ("split_type", "percentage"),
            ("participants", "1"),
            ("participants", "2"),
            ("share_1", "60"),
            ("share_2", "40"),
        ]
    )

    # Act
    result = parse_expense_form(form)

    # Assert
    assert result["shares"] == {1: Decimal(60), 2: Decimal(40)}


def test_parse_expense_form_defaults_category_to_other():
    # Arrange
    form = build_form(payer_id="1", description="Snacks", amount="5", split_type="equal", category="")

    # Act
    result = parse_expense_form(form)

    # Assert
    assert result["category"] == "other"


def test_parse_expense_form_rejects_missing_amount():
    # Arrange
    form = build_form(payer_id="1", description="Snacks", split_type="equal")

    # Act
    action = lambda: parse_expense_form(form)

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()


def test_parse_expense_form_rejects_unknown_split_type():
    # Arrange
    form = build_form(payer_id="1", description="Snacks", amount="5", split_type="weighted")

    # Act
    action = lambda: parse_expense_form(form)

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()


def test_parse_expense_form_rejects_non_numeric_payer():
    # Arrange
    form = build_form(payer_id="abc", description="Snacks", amount="5", split_type="equal")

    # Act
    action = lambda: parse_expense_form(form)

    # Assert
    with pytest.raises(InvalidExpenseError):
        action()


def test_parse_expense_form_rejects_invalid_amount_text():
    # Arrange
    form = build_form(payer_id="1", description="Snacks", amount="abc", split_type="equal")

    # Act
    action = lambda: parse_expense_form(form)

    # Assert
    with pytest.raises(InvalidSplitError):
        action()