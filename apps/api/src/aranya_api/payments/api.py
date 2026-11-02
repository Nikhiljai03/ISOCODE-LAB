import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from aranya_api.booking.models import Booking, Payment
from aranya_api.booking.schemas import PaymentConfirmation
from aranya_api.booking.states import transition, BOOKING_TRANSITIONS, PAYMENT_TRANSITIONS
from aranya_api.inventory.models import InventoryHold
from aranya_api.shared.database import get_db

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/test/confirm")
def confirm_test_payment(payload: PaymentConfirmation, db: Session = Depends(get_db)):
    existing = db.scalar(select(Payment).where(Payment.provider_event_id == payload.provider_event_id))
    if existing:
        return {"payment_id": str(existing.id), "booking_id": str(existing.booking_id), "idempotent_replay": True}

    booking = db.get(Booking, uuid.UUID(payload.booking_id))
    if booking is None:
        raise HTTPException(404, "Booking not found")
    if payload.amount != booking.total_amount:
        raise HTTPException(409, "Payment amount does not match booking")

    payment = Payment(
        booking_id=booking.id,
        provider="test",
        provider_payment_id=payload.provider_payment_id,
        provider_event_id=payload.provider_event_id,
        state="SUCCEEDED",
        amount=payload.amount,
        currency=booking.currency,
    )
    try:
        transition(booking.state, "CONFIRMED", BOOKING_TRANSITIONS)
        transition("INITIATED", "PROCESSING", PAYMENT_TRANSITIONS)
        transition("PROCESSING", "SUCCEEDED", PAYMENT_TRANSITIONS)
    except ValueError as exc:
        raise HTTPException(409, str(exc))

    booking.state = "CONFIRMED"
    if booking.hold_id:
        hold = db.get(InventoryHold, booking.hold_id)
        if hold is not None:
            hold.status = "captured"
    db.add(payment)
    db.commit()
    return {"payment_id": str(payment.id), "booking_id": str(booking.id), "idempotent_replay": False}
