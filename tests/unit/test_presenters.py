from decimal import Decimal

from app.services.settlement import Transfer
from app.web.presenters import (
    BalanceRow,
    TransferRow,
    build_balance_rows,
    build_transfer_rows,
)


def test_build_balance_rows_includes_members_without_balance():
    # Arrange
    names = {1: "Anna", 2: "Ben", 3: "Carl"}
    balances = {1: 5000, 2: -1000}

    # Act
    rows = build_balance_rows(balances, names)

    # Assert
    assert rows == [
        BalanceRow("Anna", Decimal("50.00")),
        BalanceRow("Ben", Decimal("-10.00")),
        BalanceRow("Carl", Decimal("0.00")),
    ]


def test_build_transfer_rows_replaces_ids_with_names_and_amounts():
    # Arrange
    names = {1: "Anna", 2: "Ben"}
    transfers = [Transfer(payer_id=2, receiver_id=1, amount_cents=1050)]

    # Act
    rows = build_transfer_rows(transfers, names)

    # Assert
    assert rows == [TransferRow("Ben", "Anna", Decimal("10.50"))]