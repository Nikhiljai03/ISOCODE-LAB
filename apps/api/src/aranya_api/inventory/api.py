import uuid
from datetime import date
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from aranya_api.shared.database import get_db
from aranya_api.inventory.service import hold_inventory, InventoryUnavailable, MissingConfiguration
from aranya_api.inventory.models import InventoryHold
from aranya_api.accommodations.models import DailyRate
from aranya_api.booking.models import Booking
from datetime import timedelta
from decimal import Decimal
from sqlalchemy import select
from aranya_api.shared.config import get_settings

router = APIRouter(prefix="/api/v1", tags=["inventory"])


@router.post("/holds", status_code=201)
def create_hold(category_id: uuid.UUID, arrival: date, departure: date, units: int = 1,
                guest_email: str = "guest@example.invalid", guest_name: str = "Guest",
                idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
                db: Session = Depends(get_db)):
    if not idempotency_key:
        raise HTTPException(400, "Idempotency-Key header is required")
    import hashlib
    guest_hash = hashlib.sha256(guest_email.lower().encode()).hexdigest()
    try:
        existing_hold = db.scalar(select(InventoryHold).where(InventoryHold.idempotency_key == idempotency_key))
        if existing_hold:
            db.rollback()
            return {"hold_id": str(existing_hold.id), "expires_at": existing_hold.expires_at.isoformat(), "idempotent_replay": True}
        db.rollback()
        with db.begin():
            hold = hold_inventory(db, category_id, arrival, departure, units, idempotency_key, guest_hash)
            stay_dates = [arrival + timedelta(days=i) for i in range((departure - arrival).days)]
            rates = db.scalars(select(DailyRate).where(DailyRate.category_id == category_id, DailyRate.rate_date.in_(stay_dates))).all()
            subtotal = sum((rate.base_amount * units for rate in rates), Decimal("0")).quantize(Decimal("0.01"))
            tax_rate = Decimal(str(get_settings().gst_rate_percentage)) / Decimal("100")
            tax_total = (subtotal * tax_rate).quantize(Decimal("0.01"))
            booking = Booking(
                public_reference="AR-" + str(hold.id).replace("-", "")[:16].upper(),
                guest_email_hash=guest_hash,
                guest_name=guest_name,
                guest_phone_hash="-", state="PAYMENT_PENDING", arrival=arrival, departure=departure,
                subtotal=subtotal, tax_total=tax_total, total_amount=subtotal + tax_total,
                currency=get_settings().rate_currency, hold_id=hold.id,
            )
            db.add(booking)
        db.commit()
    except InventoryUnavailable as exc:
        raise HTTPException(409, str(exc))
    except MissingConfiguration as exc:
        raise HTTPException(422, str(exc))
    return {"hold_id": str(hold.id), "booking_id": str(booking.id), "expires_at": hold.expires_at.isoformat()}


@router.post("/inventory/expire-holds")
def expire_holds(db: Session = Depends(get_db)):
    from datetime import datetime, timezone
    from sqlalchemy import update
    from aranya_api.inventory.models import InventoryHold
    result = db.execute(update(InventoryHold).where(
        InventoryHold.status == "pending", InventoryHold.expires_at <= datetime.now(timezone.utc)
    ).values(status="expired").execution_options(synchronize_session=False))
    db.commit()
    return {"expired": result.rowcount}
