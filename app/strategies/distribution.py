from decimal import ROUND_FLOOR, Decimal


def distribute_cents(total_cents: int, weights: dict[int, Decimal]) -> dict[int, int]:
    weight_sum = sum(weights.values())
    exact_shares = {
        participant_id: Decimal(total_cents) * weight / weight_sum
        for participant_id, weight in weights.items()
    }
    shares = {
        participant_id: int(share.to_integral_value(rounding=ROUND_FLOOR))
        for participant_id, share in exact_shares.items()
    }
    leftover = total_cents - sum(shares.values())
    by_remainder = sorted(
        exact_shares,
        key=lambda participant_id: exact_shares[participant_id] - shares[participant_id],
        reverse=True,
    )
    for participant_id in by_remainder[:leftover]:
        shares[participant_id] += 1
    return shares