from fastapi import APIRouter

from app.dependencies import GroupServiceDep, SettlementServiceDep
from app.money import from_cents
from app.schemas.settlement import BalanceRead, TransferRead

router = APIRouter(prefix="/groups/{group_id}", tags=["settlement"])


@router.get("/balances", response_model=list[BalanceRead])
def get_balances(
    group_id: int, groups: GroupServiceDep, settlement: SettlementServiceDep
) -> list[BalanceRead]:
    groups.get_group(group_id)
    balances = settlement.get_balances(group_id)
    return [
        BalanceRead(person_id=person_id, amount=from_cents(cents))
        for person_id, cents in balances.items()
    ]


@router.get("/settlement", response_model=list[TransferRead])
def get_settlement(
    group_id: int, groups: GroupServiceDep, settlement: SettlementServiceDep
) -> list[TransferRead]:
    groups.get_group(group_id)
    return [
        TransferRead(
            payer_id=transfer.payer_id,
            receiver_id=transfer.receiver_id,
            amount=from_cents(transfer.amount_cents),
        )
        for transfer in settlement.get_transfers(group_id)
    ]