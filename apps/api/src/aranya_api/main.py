from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aranya_api.shared.config import get_settings
from aranya_api.inventory.api import router as inventory_router
from aranya_api.enquiries.api import router as enquiry_router
from aranya_api.payments.api import router as payment_router
from aranya_api.accommodations import models as accommodation_models
from aranya_api.booking import models as booking_models
from aranya_api.inventory import models as inventory_models
from aranya_api.enquiries import models as enquiry_models

settings = get_settings()
app = FastAPI(title="ARANYA Reservations API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(inventory_router)
app.include_router(enquiry_router)
app.include_router(payment_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
