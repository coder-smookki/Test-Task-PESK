from pydantic import BaseModel, Field


class WeatherSchema(BaseModel):
    temp: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float


class CurrencySchema(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    result: float
    rate: float


class CityInfoResponse(BaseModel):
    city: str
    country_code: str
    lat: float
    lon: float
    weather: WeatherSchema | None = None
    currency: CurrencySchema | None = None
