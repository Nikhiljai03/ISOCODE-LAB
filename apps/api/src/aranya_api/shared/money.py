from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def multiply(amount: Decimal, quantity: int) -> Decimal:
    return money(amount * Decimal(quantity))
