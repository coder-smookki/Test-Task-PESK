from typing import Callable, Awaitable

from app.services.city_info import get_city_info

CityInfoCallable = Callable[..., Awaitable[dict | None]]


async def get_city_info_dep() -> CityInfoCallable:
    return get_city_info
