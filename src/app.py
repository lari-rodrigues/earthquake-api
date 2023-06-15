from fastapi import FastAPI
from datetime import date
import logging
from pydantic import BaseModel

from src.integration.earthquake_api import EarthquakeAPI

class City(BaseModel):
    name: str
    country: str

class EarthquakeSearchRequest(BaseModel):
    start_date: date
    end_date: date

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/cities")
def create_city(city: City):
    logger.info(f"City created: {city}")
    return {"message": "City created successfully"}

@app.get("/earthquakes")
def search_earthquakes(search_request: EarthquakeSearchRequest):
    return EarthquakeAPI().get_earthquake_data(search_request.start_date, search_request.end_date)