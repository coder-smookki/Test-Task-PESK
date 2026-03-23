import logging

import httpx

from app.config import settings
from app.services.http_client import get_client

logger = logging.getLogger("bot.weather")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather(lat: float, lon: float) -> dict | None:
    try:
        client = await get_client()
        resp = await client.get(
            WEATHER_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": settings.OWM_API_KEY,
                "units": "metric",
                "lang": "ru",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        result = {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        logger.info("[%.2f, %.2f] -> %s %.1f°C", lat, lon, result["description"], result["temp"])
        return result
    except httpx.TimeoutException:
        logger.error("Таймаут погоды [%.2f, %.2f]", lat, lon)
        return None
    except (httpx.HTTPError, KeyError, IndexError) as e:
        logger.error("Ошибка погоды [%.2f, %.2f]: %s", lat, lon, e)
        return None
