from pydantic import ValidationError
from aranya_api.enquiries.schemas import AIEnquiryClassification


def valid_payload():
    return {
        "category": "complaint",
        "confidence": 0.95,
        "recommended_team": "guest_relations",
        "reply_draft": "Thank you for flagging this. A member of our team will respond.",
        "missing_fields": [],
    }


def test_valid_complaint_output():
    assert AIEnquiryClassification.model_validate(valid_payload()).category == "complaint"


def test_invalid_extra_output_is_rejected():
    payload = valid_payload()
    payload["price"] = 5000
    try:
        AIEnquiryClassification.model_validate(payload)
    except ValidationError:
        return
    raise AssertionError("unexpected fields must be rejected")
