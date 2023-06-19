from datetime import date
import pandas as pd
from unittest.mock import MagicMock
from src.models.city_model import City
from src.services.earthquake_service import EarthquakeService
from src.exceptions.entity_not_found_exception import EntityNotFoundException

def test_get_nearest_earthquake_from_city():
    # arrange: Create a mock Session and City object
    mock_session = MagicMock()
    city = City(id=1, name="City", state="State", country="Country", latitude=10.0, longitude=20.0)

    # arrange: Create a test DataFrame with earthquake data
    earthquake_data = {
        "id": [1, 2, 3],
        "properties.time": [1623888000000, 1623898000000, 1623908000000],
        "properties.title": ["Earthquake 1", "Earthquake 2", "Earthquake 3"],
        "geometry.coordinates": [[38.0, 48.0], [30.0, 40.0], [35.0, 45.0]]
    }
    df = pd.DataFrame(earthquake_data)

    # arrange: Create an instance of EarthquakeService
    earthquake_service = EarthquakeService(db=mock_session)

    # arrange: Mock the get_earthquake_data method to return the test DataFrame
    earthquake_service.get_earthquake_data = lambda start_date, end_date: df
    mock_session.query.return_value.get.return_value = city

    # act
    start_date = date(2021, 6, 1)
    end_date = date(2021, 6, 30)
    result_row, result_city = earthquake_service.get_nearest_earthquake_from_city(start_date, end_date, 1)

    # assert
    assert result_row["id"] == 2
    assert result_row["properties.time"] == 1623898000000
    assert result_row["properties.title"] == "Earthquake 2"
    assert result_row["earthquake_coordinates"] == (40.0, 30.0)
    assert result_row["distance"] == 3467.9275767554286
    assert result_city == city

def test_get_nearest_earthquake_from_city_city_not_found():
    # arrange
    mock_session = MagicMock()
    earthquake_service = EarthquakeService(db=mock_session)
    mock_session.query.return_value.get.return_value = None

    # act
    start_date = date(2021, 6, 1)
    end_date = date(2021, 6, 30)
    try:
        earthquake_service.get_nearest_earthquake_from_city(start_date, end_date, 1)
    except EntityNotFoundException as e:
        # assert
        assert str(e) == "City not found."