from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aranya_api.accommodations.models import AccommodationCategory
from aranya_api.shared.database import get_db

router = APIRouter(prefix="/api/v1/accommodations", tags=["accommodations"])


@router.get("")
def list_accommodations(db: Session = Depends(get_db)):
    categories = db.query(AccommodationCategory).filter(AccommodationCategory.active.is_(True)).all()
    return [{"id": str(item.id), "code": item.code, "name": item.name, "physical_inventory_count": item.physical_inventory_count} for item in categories]


@router.get("/{category_id}")
def get_accommodation(category_id: str, db: Session = Depends(get_db)):
    category = db.get(AccommodationCategory, category_id)
    if category is None:
        raise HTTPException(404, "Accommodation not found")
    return {"id": str(category.id), "code": category.code, "name": category.name, "physical_inventory_count": category.physical_inventory_count}
