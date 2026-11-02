from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class AIEnquiryClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: Literal["room_booking", "wedding", "corporate_offsite", "complaint"]
    confidence: float = Field(ge=0.0, le=1.0)
    arrival: str | None = None
    departure: str | None = None
    guest_count: int | None = Field(default=None, ge=1)
    budget_min: float | None = Field(default=None, ge=0)
    budget_max: float | None = Field(default=None, ge=0)
    recommended_team: Literal["reservations", "events", "corporate_sales", "guest_relations"]
    missing_fields: list[str] = Field(default_factory=list)
    reply_draft: str
