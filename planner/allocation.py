"""Rule-based asset allocation. Deliberately simple and easy to argue with."""

RISK_SHIFT = {"low": -20, "medium": 0, "high": 15}


def allocation(years, risk="medium"):
    """Return (equity, debt, gold) as percentages that add up to 100.

    The base equity share depends on how long the money has to grow, then the
    risk appetite nudges it up or down. Gold is capped at 10%.
    """
    if risk not in RISK_SHIFT:
        raise ValueError(f"risk must be one of {list(RISK_SHIFT)}")

    if years <= 2:
        equity = 10
    elif years <= 5:
        equity = 30
    elif years <= 10:
        equity = 55
    else:
        equity = 70

    equity = max(0, min(90, equity + RISK_SHIFT[risk]))
    gold = min(10, 100 - equity)
    debt = 100 - equity - gold
    return equity, debt, gold
