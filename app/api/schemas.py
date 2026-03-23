from pydantic import BaseModel, Field


class WeatherSchema(BaseModel):
    temp: float = Field(description="Температура в °C", examples=[12.3])
    feels_like: float = Field(description="Ощущаемая температура в °C", examples=[9.8])
    description: str = Field(description="Текстовое описание погоды (на русском)", examples=["переменная облачность"])
    humidity: int = Field(description="Относительная влажность, %", examples=[65])
    wind_speed: float = Field(description="Скорость ветра, м/с", examples=[4.2])


class CurrencySchema(BaseModel):
    from_currency: str = Field(description="Исходная валюта", examples=["RUB"])
    to_currency: str = Field(description="Целевая валюта страны города", examples=["EUR"])
    amount: float = Field(description="Исходная сумма в рублях", examples=[5000.0])
    result: float = Field(description="Результат конвертации в целевой валюте", examples=[48.72])
    rate: float = Field(description="Курс: 1 RUB = N целевой валюты", examples=[0.009744])


class CityInfoResponse(BaseModel):
    city: str = Field(description="Название города", examples=["Berlin"])
    country_code: str = Field(description="ISO 3166-1 alpha-2 код страны", examples=["DE"])
    lat: float = Field(description="Широта", examples=[52.52])
    lon: float = Field(description="Долгота", examples=[13.41])
    weather: WeatherSchema | None = Field(None, description="Данные о погоде (null если запрос не удался)")
    currency: CurrencySchema | None = Field(None, description="Данные о конвертации (null если валюта не определена)")

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }
