BOOKING_TRANSITIONS = {
    "DRAFT": {"PAYMENT_PENDING"},
    "PAYMENT_PENDING": {"CONFIRMED", "HOLD_EXPIRED", "PAYMENT_FAILED"},
    "PAYMENT_FAILED": {"PAYMENT_PENDING"},
    "CONFIRMED": {"CANCEL_REQUESTED", "COMPLETED", "NO_SHOW"},
    "CANCEL_REQUESTED": {"CANCELLED"},
    "CANCELLED": set(),
    "HOLD_EXPIRED": set(),
    "COMPLETED": set(),
    "NO_SHOW": set(),
}

PAYMENT_TRANSITIONS = {
    "INITIATED": {"PROCESSING"},
    "PROCESSING": {"SUCCEEDED", "FAILED", "CANCELLED"},
    "FAILED": set(),
    "CANCELLED": set(),
    "SUCCEEDED": {"PARTIALLY_REFUNDED", "REFUNDED"},
    "PARTIALLY_REFUNDED": {"REFUNDED"},
    "REFUNDED": set(),
}


def transition(current: str, target: str, transitions: dict[str, set[str]]) -> None:
    if target not in transitions.get(current, set()):
        raise ValueError(f"Invalid transition: {current} -> {target}")
