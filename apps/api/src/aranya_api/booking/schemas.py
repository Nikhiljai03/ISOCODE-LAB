from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class HoldNight(BaseModel):
    category_id: str
    stay_date: date


class CreateHoldRequest(BaseModel):
    category_id: str
    arrival: date
    departure: date
    units: int = Field(default=1, ge=1, le=10)
    guest_email: str
    guest_name: str

    @field_validator("departure")
    @classmethod
    def departure_after_arrival(cls, departure: date, info) -> date:
        if "arrival" in info.data and departure <= info.data["arrival"]:
            raise ValueError("departure must be after arrival")
        return departure


class MoneyNight(BaseModel):
    stay_date: date
    base_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal


class HoldResponse(BaseModel):
    hold_id: str
    expires_at: str


class PaymentConfirmation(BaseModel):
    booking_id: str
    provider_payment_id: str
    provider_event_id: str
    amount: Decimal


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    public_reference: str
    state: str
    total_amount: Decimal
