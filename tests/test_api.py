from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.api.__main__ import app

MOCK_CITY_DATA = {
    "city": "Berlin",
    "country_code": "DE",
    "lat": 52.52,
    "lon": 13.41,
    "weather": {
        "temp": 12.3,
        "feels_like": 9.8,
        "description": "переменная облачность",
        "humidity": 65,
        "wind_speed": 4.2,
    },
    "currency": {
        "from_currency": "RUB",
        "to_currency": "EUR",
        "amount": 5000.0,
        "result": 48.72,
        "rate": 0.009744,
    },
}


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_city_info_empty_city_returns_422(client):
    response = client.get("/api/v1/city-info", params={"city": "", "amount": 5000})
    assert response.status_code == 422


def test_city_info_not_found_returns_404(client):
    with patch("app.api.router.get_city_info", new=AsyncMock(return_value=None)):
        response = client.get("/api/v1/city-info", params={"city": "НесуществующийГород", "amount": 1000})
    assert response.status_code == 404
    assert response.json()["detail"] == "Город не найден"


def test_city_info_success_returns_200(client):
    with patch("app.api.router.get_city_info", new=AsyncMock(return_value=MOCK_CITY_DATA)):
        response = client.get("/api/v1/city-info", params={"city": "Берлин", "amount": 5000})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Berlin"
    assert data["country_code"] == "DE"
    assert data["weather"]["temp"] == 12.3
    assert data["currency"]["to_currency"] == "EUR"
