from fastapi.encoders import jsonable_encoder
from src.services.city_service import CityService
from src.models.city_model import City
from src.schemas.city_request import CityRequest

def test_create_city(client, test_db, monkeypatch):
    # arrange
    mock_city = City(name='City', state='State', country='Country')
    monkeypatch.setattr(CityService, 'create_city', lambda self, city_request: mock_city)

    # act
    city_request = CityRequest(name='City', state='State', country='Country')
    response = client.post('/cities', json=city_request.dict())
    
    # assert
    assert response.status_code == 200
    assert response.json() == {"message": f"City created successfully with ID {mock_city.id}!"}


def test_get_cities(client, test_db, monkeypatch):
    # arrange
    mock_cities = [City(name='City', state='State', country='Country')]
    monkeypatch.setattr(CityService, 'get_all_cities', lambda self: mock_cities)

    # act
    response = client.get('/cities')

    # assert
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(mock_cities)