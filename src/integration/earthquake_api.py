import requests
from datetime import date
import logging


class EarthquakeAPI:
    USGS_API_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson'
    DEFAULT_MIN_MAGNITUDE = 5

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_earthquake_data(self, start_time: date, end_time: date, min_magnitude : float =  DEFAULT_MIN_MAGNITUDE):
        start_time_str = start_time.strftime('%Y-%m-%d')
        end_time_str = end_time.strftime('%Y-%m-%d')

        params = {
            'starttime': start_time_str,
            'endtime': end_time_str,
            'minmagnitude': min_magnitude,
            'orderby': 'time'
        }

        try:
            response = requests.get(self.USGS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred: {e}")
            raise

        except ValueError:
            self.logger.error("Error: Invalid JSON response")
            raise
