from datetime import date
from sqlalchemy.orm import Session
import pandas as pd
from geopy.distance import geodesic
from src.models.city_model import City
from src.integration.earthquake_api import EarthquakeAPI
from src.exceptions.entity_not_found_exception import EntityNotFoundException
import logging

DEFAULT_MIN_MAGNITUDE = 5

class EarthquakeService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def get_earthquake_data(self,
                            start_date: date,
                            end_date: date):
        self.logger.info("Getting earthquake data")
        earthquakes_result = EarthquakeAPI().get_earthquake_data(start_date, end_date, DEFAULT_MIN_MAGNITUDE)
        df = pd.json_normalize(earthquakes_result, record_path =["features"])
        df = df[["id", "properties.time", "properties.title", "geometry.coordinates"]]

        return df

    def get_nearest_earthquake_from_city(self, 
                                         start_date: date,
                                         end_date: date,
                                         city_id: int):

        self.logger.info("Getting nearest earthquake from city")
        df = self.get_earthquake_data(start_date, end_date)
        city = self.db.query(City).get(city_id)
        if not city:
            raise EntityNotFoundException("City not found.")

        # get a tuple (latitude, longitude) from earthquakes [longitude, latitude, depth]
        df["earthquake_coordinates"] = df["geometry.coordinates"].apply(lambda x: (x[1], x[0]))
        df["distance"] = df.apply(lambda row: geodesic((city.latitude, city.longitude), row["earthquake_coordinates"]).km, axis=1)

        min_distance_row = df.loc[df["distance"].idxmin()]

        return min_distance_row, city