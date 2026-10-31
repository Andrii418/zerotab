from decimal import Decimal

import pytest

from app.money import from_cents, to_cents, to_money


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("10.005", Decimal("10.01")),
        ("10.004", Decimal("10.00")),
        (7, Decimal("7.00")),
        (Decimal("0.1"), Decimal("0.10")),
    ],
)
def test_to_money_rounds_half_up_to_two_places(raw_value, expected):
    # Arrange
    value = raw_value

    # Act
    result = to_money(value)

    # Assert
    assert result == expected
    assert result.as_tuple().exponent == -2


def test_to_cents_converts_amount_to_integer_cents():
    # Arrange
    amount = Decimal("19.99")

    # Act
    cents = to_cents(amount)

    # Assert
    assert cents == 1999


def test_from_cents_converts_cents_to_decimal_amount():
    # Arrange
    cents = 5

    # Act
    amount = from_cents(cents)

    # Assert
    assert amount == Decimal("0.05")


def test_cents_round_trip_preserves_amount():
    # Arrange
    amount = Decimal("1234.56")

    # Act
    result = from_cents(to_cents(amount))

    # Assert
    assert result == amount