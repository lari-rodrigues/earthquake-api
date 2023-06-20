from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.earthquake_service import EarthquakeService
from src.exceptions.entity_not_found_exception import EntityNotFoundException
from src.exceptions.empty_data_from_api import EmptyDataFromAPI

router = APIRouter(prefix="/earthquakes")


@router.get(path="", description="Find the nearest earthquake above 5.0 between the dates in relation to the given city.")
def search_earthquakes(start_date: date = Query(None, description="Start date"), 
                       end_date: date = Query(None, description="End date"), 
                       city: int = Query(None, description="City ID registered on system"),
                       db: Session = Depends(get_db)):
    try:
        min_distance_row, city = EarthquakeService(db).get_nearest_earthquake_from_city(start_date, end_date, city)
    except (EntityNotFoundException, EmptyDataFromAPI):
        return {}
    
    earthquake_dt = date.fromtimestamp(min_distance_row['properties.time'] / 1000) # convert to seconds and then to date
    
    return {"message": f"""Results between {start_date.strftime('%B %d, %Y')} and {end_date.strftime('%B %d, %Y')}: 
    The closest Earthquake to {city.name} was an {min_distance_row['properties.title']} on {earthquake_dt.strftime('%B %d, %Y')}"""}