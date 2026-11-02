from decimal import Decimal
import pytest
from aranya_api.booking.states import transition, BOOKING_TRANSITIONS, PAYMENT_TRANSITIONS
from aranya_api.enquiries.schemas import AIEnquiryClassification
from aranya_api.shared.money import money, multiply


def test_booking_confirm_transition():
    transition("PAYMENT_PENDING", "CONFIRMED", BOOKING_TRANSITIONS)


def test_invalid_booking_transition_rejected():
    with pytest.raises(ValueError):
        transition("DRAFT", "CONFIRMED", BOOKING_TRANSITIONS)


def test_payment_terminal_succeeds():
    transition("PROCESSING", "SUCCEEDED", PAYMENT_TRANSITIONS)


def test_decimal_money_never_float():
    assert money(Decimal("19.99") * 3) == Decimal("59.97")
    assert multiply(Decimal("100.00"), 3) == Decimal("300.00")


def test_ai_schema_rejects_extra_fields():
    with pytest.raises(Exception):
        AIEnquiryClassification.model_validate({
            "category": "room_booking",
            "confidence": 0.9,
            "recommended_team": "reservations",
            "reply_draft": "We will help",
            "invented_price": "1000",
        })
