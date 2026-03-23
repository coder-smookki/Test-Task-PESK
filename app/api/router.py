from fastapi import APIRouter, Query, Depends, HTTPException

from app.api.schemas import CityInfoResponse
from app.api.dependencies import get_city_info_dep, CityInfoCallable

router = APIRouter(prefix="/api/v1", tags=["city"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/city-info", response_model=CityInfoResponse)
async def city_info(
    city: str = Query(..., description="Название города"),
    amount: float = Query(1000, description="Сумма в RUB"),
    service: CityInfoCallable = Depends(get_city_info_dep),
):
    result = await service(city, amount)
    if result is None:
        raise HTTPException(status_code=404, detail="Город не найден")
    return result
