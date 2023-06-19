from sqlalchemy.orm import Session
from geopy.geocoders import Nominatim
from src.schemas.city_request import CityRequest
from src.models.city_model import City
from src.exceptions.entity_not_found_exception import EntityNotFoundException
import logging


class CityService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)


    def find_location(self, city: str, state: str, country: str):
        self.logger.info("Finding location")
        geolocator = Nominatim(user_agent=__name__)
        location = geolocator.geocode(f"{city}, {state}, {country}")
        if not location:
            raise EntityNotFoundException("Location not found.")
        
        return location

    def create_city(self, city_request: CityRequest):
        self.logger.info("Creating city")
        location = self.find_location(city_request.name, city_request.state, city_request.country)

        city = City(name=city_request.name, 
                    state=city_request.state,
                    country=city_request.country,
                    latitude=location.latitude,
                    longitude=location.longitude)

        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)

        return city

    def get_all_cities(self):
        self.logger.info("Getting all cities")
        return self.db.query(City).all()