import asyncio
import logging

from app.services.currency import convert_currency
from app.services.geo import geocode
from app.services.weather import get_weather
from app.utils.cache import TTLCache

logger = logging.getLogger("bot.city_info")

_cache = TTLCache(ttl=300.0)


async def get_city_info(
    city: str,
    amount: float,
    force: bool = False,
) -> dict | None:
    key = f"{city.strip().lower()}:{float(amount)}"

    if not force:
        cached = _cache.get(key)
        if cached is not None:
            logger.info("Кэш-хит: %s", key)
            return cached

    geo = await geocode(city)
    if not geo:
        return None

    weather, currency = await asyncio.gather(
        get_weather(geo["lat"], geo["lon"]),
        convert_currency(geo["country_code"], amount),
    )

    result = {
        "city": geo["city"],
        "country_code": geo["country_code"],
        "lat": geo["lat"],
        "lon": geo["lon"],
        "weather": weather,
        "currency": currency,
    }

    _cache.set(key, result)
    return result
