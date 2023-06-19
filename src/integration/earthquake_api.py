import requests
import requests_cache

from datetime import date
import logging


class EarthquakeAPI:
    USGS_API_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests_cache.CachedSession(__name__)


    def get_earthquake_data(self, start_time: date, end_time: date, min_magnitude : float):
        self.logger.info("Getting earthquake data")
        start_time_str = start_time.strftime('%Y-%m-%d')
        end_time_str = end_time.strftime('%Y-%m-%d')

        params = {
            'starttime': start_time_str,
            'endtime': end_time_str,
            'minmagnitude': min_magnitude,
            'orderby': 'time'
        }

        try:
            response = self.session.get(self.USGS_API_URL, params=params)
            response.raise_for_status()

            self.logger.info("Data collected from cache" if response.from_cache else "Data collected from API")

            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred: {e}")
            raise

        except ValueError:
            self.logger.error("Error: Invalid JSON response")
            raise
