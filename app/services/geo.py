import logging

import httpx

from app.config import settings
from app.services.http_client import get_client

logger = logging.getLogger("bot.geo")

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"


async def geocode(city: str) -> dict | None:
    try:
        client = await get_client()
        resp = await client.get(
            GEO_URL,
            params={"q": city, "limit": 1, "appid": settings.OWM_API_KEY},
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            logger.warning("Город '%s' не найден", city)
            return None
        item = data[0]
        result = {
            "city": item.get("local_names", {}).get("ru", item["name"]),
            "country_code": item["country"],
            "lat": item["lat"],
            "lon": item["lon"],
        }
        logger.info("%s -> %s [%.4f, %.4f]", city, result["country_code"], result["lat"], result["lon"])
        return result
    except httpx.TimeoutException:
        logger.error("Таймаут геокодинга '%s'", city)
        return None
    except (httpx.HTTPError, KeyError, IndexError) as e:
        logger.error("Ошибка геокодинга '%s': %s", city, e)
        return None
