from fastapi import FastAPI
from datetime import date
import logging
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


from src.integration.earthquake_api import EarthquakeAPI
from src.database.database import get_db
from src.domain.city import City

class CityRequest(BaseModel):
    name: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    country: str= Field(..., min_length=1)

class EarthquakeSearchRequest(BaseModel):
    start_date: date
    end_date: date
    city: int = Field(..., gt=-1, description="City ID at system")

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/cities")
def create_city(city_request: CityRequest, db: Session = Depends(get_db)):
    city = City()
    city.name = city_request.name
    city.state = city_request.state
    city.country = city_request.country
    geolocator = Nominatim(user_agent=__name__)
    location = geolocator.geocode(f"{city.name}, {city.state}, {city.country}")
    if not location:
        return {"message": f"Location not found."}

    city.latitude = location.latitude
    city.longitude = location.longitude
    db.add(city)
    db.commit()
    db.refresh(city)
    return {"message": f"City created successfully with ID {city.id}!"}

@app.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@app.get("/earthquakes")
def search_earthquakes(search_request: EarthquakeSearchRequest, db: Session = Depends(get_db)):
    earthquakes_result = EarthquakeAPI().get_earthquake_data(search_request.start_date, search_request.end_date)
    df = pd.json_normalize(earthquakes_result, record_path =["features"])
    df = df[["id", "properties.time", "properties.title", "geometry.coordinates"]]

    city = db.query(City).get(search_request.city)
    if not city:
        return {"message": "City not found"}

    # get a tuple (latitude, longitude) from earthquakes [longitude, latitude, depth]
    df["earthquake_coordinates"] = df["geometry.coordinates"].apply(lambda x: (x[1], x[0]))
    df["distance"] = df.apply(lambda row: geodesic((city.latitude, city.longitude), row["earthquake_coordinates"]).km, axis=1)

    min_distance_row = df.loc[df["distance"].idxmin()]
    print(min_distance_row)
    earthquake_dt = date.fromtimestamp(min_distance_row['properties.time'] / 1000) # convert to seconds and then to date
    print(earthquake_dt)
    return {"message": f"""Results between {search_request.start_date.strftime('%B %d, %Y')} and {search_request.end_date.strftime('%B %d, %Y')}: 
    The closest Earthquake to {city.name} was an {min_distance_row['properties.title']} on {earthquake_dt.strftime('%B %d, %Y')}"""}

#http://localhost:8000/earthquakes?start_date=X&end_date=Y&city=2
