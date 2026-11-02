import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from aranya_api.enquiries.ai import AIProviderError, classify
from aranya_api.enquiries.models import Enquiry, EnquiryAlert, EnquiryDraft
from aranya_api.shared.config import get_settings
from aranya_api.shared.database import get_db

router = APIRouter(prefix="/api/v1/enquiries", tags=["enquiries"])


class EnquiryCreate(BaseModel):
    source: str = Field(pattern="^(website|email|whatsapp)$")
    external_id: str
    sender_name: str
    sender_contact: str
    message: str


@router.post("", status_code=201)
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)):
    enquiry = Enquiry(**payload.model_dump(), status="AI_PENDING")
    db.add(enquiry)
    db.flush()
    try:
        result = classify(enquiry.message, enquiry.sender_name)
        enquiry.category = result.category
        enquiry.confidence = result.confidence
        enquiry.extracted = result.model_dump(exclude={"reply_draft", "category", "confidence"})
        db.add(EnquiryDraft(enquiry_id=enquiry.id, content=result.reply_draft, status="draft"))
        if result.category == "complaint":
            db.add(EnquiryAlert(enquiry_id=enquiry.id))
            enquiry.status = "complaint"
        elif result.confidence < get_settings().ai_low_confidence_threshold:
            enquiry.status = "unsorted"
        else:
            enquiry.status = "classified"
    except AIProviderError as exc:
        enquiry.status = "AI_ERROR"
    db.commit()
    return {"id": str(enquiry.id), "status": enquiry.status}


@router.post("/{enquiry_id}/drafts/{draft_id}/approve")
def approve_draft(enquiry_id: uuid.UUID, draft_id: uuid.UUID, db: Session = Depends(get_db)):
    draft = db.get(EnquiryDraft, draft_id)
    if draft is None or draft.enquiry_id != enquiry_id:
        raise HTTPException(404, "Draft not found")
    draft.status = "approved"
    db.commit()
    return {"status": "approved"}
