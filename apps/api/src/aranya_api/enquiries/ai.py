from google import genai
from pydantic import ValidationError
from aranya_api.enquiries.schemas import AIEnquiryClassification
from aranya_api.shared.config import get_settings


SYSTEM_PROMPT = """Classify the enquiry and return strict JSON only.
Never invent room availability, prices, taxes, GST, or event promises.
The reply_draft may ask for missing information but must not state commercial facts.
Return confidence below 0.70 when ambiguous."""


class AIProviderError(RuntimeError):
    pass


def classify(message: str, sender_name: str) -> AIEnquiryClassification:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise AIProviderError("Gemini API key is not configured")
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=f"{SYSTEM_PROMPT}\nSender: {sender_name}\nMessage:\n{message}",
            config={"response_mime_type": "application/json"},
        )
        return AIEnquiryClassification.model_validate_json(response.text)
    except ValidationError as exc:
        raise AIProviderError("Gemini returned invalid structured output") from exc
    except AIProviderError:
        raise
    except Exception as exc:
        raise AIProviderError("Gemini classification failed") from exc
