from fastapi import APIRouter, Query, HTTPException

from app.api.schemas import CityInfoResponse
from app.services.city_info import get_city_info

router = APIRouter(prefix="/api/v1", tags=["city"])


@router.get(
    "/health",
    summary="Проверка работоспособности",
    description="Возвращает `{\"status\": \"ok\"}` если сервис запущен.",
    responses={200: {"content": {"application/json": {"example": {"status": "ok"}}}}},
)
async def health():
    return {"status": "ok"}


@router.get(
    "/city-info",
    summary="Информация о городе",
    description=(
        "Геокодирует название города, получает текущую погоду через OpenWeatherMap "
        "и конвертирует сумму из RUB в местную валюту через ExchangeRate-API. "
        "Результат кешируется на 5 минут."
    ),
    response_model=CityInfoResponse,
    responses={404: {"description": "Город не найден или геокодирование не вернуло результатов"}},
)
async def city_info(
    city: str = Query(..., min_length=1, max_length=100, description="Название города на любом языке", examples=["Берлин"]),
    amount: float = Query(1000, gt=0, description="Сумма в рублях для конвертации в местную валюту", examples=[5000]),
):
    result = await get_city_info(city.strip(), amount)
    if result is None:
        raise HTTPException(status_code=404, detail="Город не найден")
    return result
