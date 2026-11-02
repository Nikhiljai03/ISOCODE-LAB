import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from aranya_api.accommodations.models import DailyRate, InventoryNight, WebsiteAllotmentNight, BlackoutDate
from aranya_api.booking.models import BookingNight
from aranya_api.inventory.models import InventoryHold, InventoryHoldNight
from aranya_api.shared.config import get_settings
from aranya_api.shared.money import money


class InventoryUnavailable(Exception):
    pass


class MissingConfiguration(Exception):
    pass


def nights_between(arrival: date, departure: date) -> list[date]:
    if departure <= arrival:
        raise ValueError("departure must be after arrival")
    return [arrival + timedelta(days=i) for i in range((departure - arrival).days)]


def hold_inventory(db: Session, category_id: uuid.UUID, arrival: date, departure: date,
                   units: int, idempotency_key: str, guest_email_hash: str) -> InventoryHold:
    dates = nights_between(arrival, departure)
    keys = sorted((category_id, stay_date) for stay_date in dates)

    try:
        for category, stay_date in keys:
            db.execute(
                func.pg_advisory_xact_lock(
                    func.hashtext(str(category)), func.hashtext(str(stay_date))
                )
            )
        db.flush()

        for category, stay_date in keys:
            allotment = db.scalar(select(WebsiteAllotmentNight).where(
                WebsiteAllotmentNight.category_id == category,
                WebsiteAllotmentNight.allotment_date == stay_date,
            ))
            if allotment is None:
                raise MissingConfiguration(f"website allotment missing for {stay_date}")
            rate = db.scalar(select(DailyRate).where(
                DailyRate.category_id == category, DailyRate.rate_date == stay_date
            ))
            if rate is None:
                raise MissingConfiguration(f"rate missing for {stay_date}")
            blackout = db.scalar(select(BlackoutDate).where(
                BlackoutDate.category_id == category, BlackoutDate.blackout_date == stay_date
            ))
            if blackout is not None:
                raise InventoryUnavailable(f"stay date is blacked out: {stay_date}")

        rows = db.scalars(select(WebsiteAllotmentNight).where(
            WebsiteAllotmentNight.category_id.in_([category_id]),
            WebsiteAllotmentNight.allotment_date.in_(dates),
        ).order_by(WebsiteAllotmentNight.category_id, WebsiteAllotmentNight.allotment_date).with_for_update()).all()
        found = {(row.category_id, row.allotment_date) for row in rows}
        if found != set(keys):
            raise MissingConfiguration("one or more allocation rows are missing")

        usage = {}
        for key in keys:
            category, stay_date = key
            confirmed = db.scalar(select(func.coalesce(func.sum(BookingNight.units), 0)).join(
                __import__('aranya_api.booking.models', fromlist=['Booking']).Booking,
                BookingNight.booking_id == __import__('aranya_api.booking.models', fromlist=['Booking']).Booking.id,
            ).where(
                BookingNight.category_id == category,
                BookingNight.stay_date == stay_date,
                __import__('aranya_api.booking.models', fromlist=['Booking']).Booking.state == "CONFIRMED",
            )) or 0
            held = db.scalar(select(func.coalesce(func.sum(InventoryHoldNight.units), 0)).join(
                InventoryHold, InventoryHoldNight.hold_id == InventoryHold.id
            ).where(
                InventoryHoldNight.category_id == category,
                InventoryHoldNight.stay_date == stay_date,
                InventoryHold.status == "pending",
                InventoryHold.expires_at > datetime.now(timezone.utc),
            )) or 0
            usage[key] = int(confirmed) + int(held)

        allotments = {(row.category_id, row.allotment_date): row.website_units for row in rows}
        if any(usage[key] + units > allotments[key] for key in keys):
            raise InventoryUnavailable("one or more nights are no longer available")

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=get_settings().hold_duration_minutes)
        hold = InventoryHold(
            idempotency_key=idempotency_key,
            guest_email_hash=guest_email_hash,
            units=units,
            status="pending",
            expires_at=expires_at,
        )
        db.add(hold)
        db.flush()
        for category, stay_date in keys:
            db.add(InventoryHoldNight(hold_id=hold.id, category_id=category, stay_date=stay_date, units=units))
        db.flush()
        return hold
    except (InventoryUnavailable, MissingConfiguration):
        raise
