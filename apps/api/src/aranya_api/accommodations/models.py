import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from aranya_api.shared.database import Base


class AccommodationCategory(Base):
    __tablename__ = "accommodation_categories"
    __table_args__ = (CheckConstraint("physical_inventory_count >= 0", name="ck_category_inventory_nonnegative"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    physical_inventory_count: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class InventoryNight(Base):
    __tablename__ = "inventory_nights"
    __table_args__ = (
        UniqueConstraint("category_id", "inventory_date", name="uq_inventory_category_date"),
        CheckConstraint("physical_total >= 0", name="ck_inventory_physical_nonnegative"),
        CheckConstraint("out_of_service >= 0", name="ck_inventory_oos_nonnegative"),
        CheckConstraint("reserved_by_other_channels >= 0", name="ck_inventory_other_nonnegative"),
        CheckConstraint("out_of_service + reserved_by_other_channels <= physical_total", name="ck_inventory_counts"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accommodation_categories.id"), nullable=False)
    inventory_date: Mapped[date] = mapped_column(Date, nullable=False)
    physical_total: Mapped[int] = mapped_column(Integer, nullable=False)
    out_of_service: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_by_other_channels: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class WebsiteAllotmentNight(Base):
    __tablename__ = "website_allotment_nights"
    __table_args__ = (
        UniqueConstraint("category_id", "allotment_date", name="uq_allotment_category_date"),
        CheckConstraint("website_units >= 0", name="ck_allotment_nonnegative"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accommodation_categories.id"), nullable=False)
    allotment_date: Mapped[date] = mapped_column(Date, nullable=False)
    website_units: Mapped[int] = mapped_column(Integer, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class DailyRate(Base):
    __tablename__ = "daily_rates"
    __table_args__ = (
        UniqueConstraint("category_id", "rate_date", name="uq_rate_category_date"),
        CheckConstraint("base_amount >= 0", name="ck_rate_nonnegative"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accommodation_categories.id"), nullable=False)
    rate_date: Mapped[date] = mapped_column(Date, nullable=False)
    base_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)


class BlackoutDate(Base):
    __tablename__ = "blackout_dates"
    __table_args__ = (UniqueConstraint("category_id", "blackout_date", name="uq_blackout_category_date"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accommodation_categories.id"), nullable=False)
    blackout_date: Mapped[date] = mapped_column(Date, nullable=False)
