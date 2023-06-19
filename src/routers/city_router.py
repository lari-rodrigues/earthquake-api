from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.city_request import CityRequest
from src.config.database import get_db
from src.services.city_service import CityService

router = APIRouter(prefix="/cities")


@router.post(path="", description="Create a new city. Application will enrich data with coordinates.")
def create_city(city_request: CityRequest, db: Session = Depends(get_db)):
    city = CityService(db).create_city(city_request)
    return {"message": f"City created successfully with ID {city.id}!"}

@router.get(path="", description="Get all cities.")
def get_cities(db: Session = Depends(get_db)):
    return CityService(db).get_all_cities()