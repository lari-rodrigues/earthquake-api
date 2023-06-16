from fastapi import FastAPI
from datetime import date
import logging
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.integration.earthquake_api import EarthquakeAPI
from src.database.database import get_db
from src.domain.city import City

class CityRequest(BaseModel):
    name: str
    state: str
    country: str

class EarthquakeSearchRequest(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/cities")
def create_city(city_request: CityRequest, db: Session = Depends(get_db)):
    city = City()
    city.name = city_request.name
    city.state = city_request.state
    city.country = city_request.country
    db.add(city)
    db.commit()
    db.refresh(city)
    return {"message": f"City created successfully with ID {city.id}!"}

@app.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@app.get("/earthquakes")
def search_earthquakes(search_request: EarthquakeSearchRequest):
    return EarthquakeAPI().get_earthquake_data(search_request.start_date, search_request.end_date)