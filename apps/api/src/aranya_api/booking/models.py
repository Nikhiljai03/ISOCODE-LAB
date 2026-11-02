import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from aranya_api.shared.database import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="ck_booking_subtotal_nonnegative"),
        CheckConstraint("tax_total >= 0", name="ck_booking_tax_nonnegative"),
        CheckConstraint("total_amount >= 0", name="ck_booking_total_nonnegative"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_reference: Mapped[str] = mapped_column(String(24), unique=True, nullable=False)
    guest_email_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    guest_name: Mapped[str] = mapped_column(String(150), nullable=False)
    guest_phone_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(30), default="DRAFT", nullable=False)
    arrival: Mapped[date] = mapped_column(Date, nullable=False)
    departure: Mapped[date] = mapped_column(Date, nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    hold_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("inventory_holds.id", use_alter=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class BookingNight(Base):
    __tablename__ = "booking_nights"
    __table_args__ = (
        UniqueConstraint("booking_id", "category_id", "stay_date", name="uq_booking_night"),
        CheckConstraint("units > 0", name="ck_booking_night_positive"),
        CheckConstraint("base_amount >= 0 AND tax_amount >= 0 AND total_amount >= 0", name="ck_booking_night_money_nonnegative"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accommodation_categories.id"), nullable=False)
    stay_date: Mapped[date] = mapped_column(Date, nullable=False)
    units: Mapped[int] = mapped_column(Integer, nullable=False)
    base_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_payment_amount_nonnegative"),
        UniqueConstraint("provider", "provider_payment_id", name="uq_provider_payment"),
        UniqueConstraint("provider_event_id", name="uq_provider_event"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    provider_payment_id: Mapped[str] = mapped_column(String(150), nullable=False)
    provider_event_id: Mapped[str] = mapped_column(String(150), nullable=False)
    state: Mapped[str] = mapped_column(String(30), default="INITIATED", nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
