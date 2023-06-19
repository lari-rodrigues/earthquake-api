from unittest.mock import MagicMock
from src.services.city_service import CityService
from src.schemas.city_request import CityRequest
from src.models.city_model import City
from src.exceptions.entity_not_found_exception import EntityNotFoundException

def test_find_location_success(monkeypatch):
    # arrange
    mock_location = MagicMock()
    geolocator = MagicMock()
    geolocator.geocode = MagicMock(return_value=mock_location)
    monkeypatch.setattr("src.services.city_service.Nominatim", MagicMock(return_value=geolocator))

    # act
    city_service = CityService(db=MagicMock())
    result = city_service.find_location("City", "State", "Country")

    # assert
    assert result == mock_location

def test_find_location_not_found(monkeypatch):
    # arrange
    geolocator = MagicMock()
    geolocator.geocode = MagicMock(return_value=None)
    monkeypatch.setattr("src.services.city_service.Nominatim", MagicMock(return_value=geolocator))

    # act
    city_service = CityService(db=MagicMock())
    try:
        city_service.find_location("City", "State", "Country")
    except EntityNotFoundException as e:
        # assert
        assert str(e) == "Location not found."

def test_create_city():
    # arrange
    mock_location = MagicMock(latitude=10.0, longitude=20.0)
    city_service = CityService(db=MagicMock())
    city_service.find_location = MagicMock(return_value=mock_location)

    # act
    city_request = CityRequest(name="City", state="State", country="Country")
    result = city_service.create_city(city_request)

    # assert
    assert isinstance(result, City)
    assert result.name == "City"
    assert result.state == "State"
    assert result.country == "Country"
    assert result.latitude == 10.0
    assert result.longitude == 20.0

def test_get_all_cities():
    # arrange
    mock_cities = [
        City(name="City1", state="State1", country="Country1", latitude=10.0, longitude=20.0),
        City(name="City2", state="State2", country="Country2", latitude=30.0, longitude=40.0)
    ]
    city_service = CityService(db=MagicMock())
    city_service.db.query.return_value.all = MagicMock(return_value=mock_cities)

    # act
    result = city_service.get_all_cities()

    # assert
    assert result == mock_cities