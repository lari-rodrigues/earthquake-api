from unittest.mock import MagicMock
from unittest import mock

from src.services.earthquake_service import EarthquakeService
from src.exceptions.entity_not_found_exception import EntityNotFoundException
from src.exceptions.empty_data_from_api import EmptyDataFromAPI

def test_search_earthquakes(client, test_db, monkeypatch):
    # arrange
    mock_min_distance_row = {
        'properties.time': 1641042925380,
        'properties.title': 'M 5.2 - Badakhshan, Afghanistan'
    }
    mock_city = MagicMock()
    mock_city.name = 'City Name'
    monkeypatch.setattr(EarthquakeService, 'get_nearest_earthquake_from_city', lambda self, start_date, end_date, city: (mock_min_distance_row, mock_city))


    # act
    response = client.get('/earthquakes', params={'start_date': '2022-01-01', 'end_date': '2022-12-31', 'city': 1})

    # assert
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Results between January 01, 2022 and December 31, 2022: \n    The closest Earthquake to City Name was an M 5.2 - Badakhshan, Afghanistan on January 01, 2022'
    }

def test_search_earthquakes_city_not_found_exception(client):
    # arrange
    with mock.patch.object(EarthquakeService, 'get_nearest_earthquake_from_city', side_effect=EntityNotFoundException): 
        # act
        response = client.get('/earthquakes', params={'start_date': '2022-01-01', 'end_date': '2022-12-31', 'city': 1})
        
        # assert
        assert response.status_code == 200
        assert response.json() == {}

def test_search_earthquakes_empty_data_from_api_exception(client):
    # arrange
    with mock.patch.object(EarthquakeService, 'get_nearest_earthquake_from_city', side_effect=EmptyDataFromAPI): 
        # act
        response = client.get('/earthquakes', params={'start_date': '2022-01-01', 'end_date': '2022-12-31', 'city': 1})
        
        # assert
        assert response.status_code == 200
        assert response.json() == {}