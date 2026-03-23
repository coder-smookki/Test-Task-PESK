import logging

import httpx

from app.config import settings
from app.services.http_client import get_client
from app.utils.country_currencies import COUNTRY_CURRENCIES

logger = logging.getLogger("bot.currency")

PAIR_URL = "https://v6.exchangerate-api.com/v6/{key}/pair/{src}/{dst}/{amount}"


async def convert_currency(
    country_code: str,
    amount: float,
) -> dict | None:
    currency = COUNTRY_CURRENCIES.get(country_code)
    if not currency:
        logger.warning("Валюта для %s не найдена", country_code)
        return None

    if currency == "RUB":
        return {
            "from_currency": "RUB",
            "to_currency": "RUB",
            "amount": amount,
            "result": amount,
            "rate": 1.0,
        }

    try:
        client = await get_client()
        url = PAIR_URL.format(
            key=settings.EXCHANGE_API_KEY,
            src="RUB",
            dst=currency,
            amount=amount,
        )
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data.get("result") != "success":
            logger.error("API вернул ошибку для %s->%s", "RUB", currency)
            return None
        result = {
            "from_currency": "RUB",
            "to_currency": currency,
            "amount": amount,
            "result": data["conversion_result"],
            "rate": data["conversion_rate"],
        }
        logger.info("%.0f RUB -> %.2f %s (rate %.4f)", amount, result["result"], currency, result["rate"])
        return result
    except httpx.TimeoutException:
        logger.error("Таймаут конвертации RUB->%s", currency)
        return None
    except (httpx.HTTPError, KeyError) as e:
        logger.error("Ошибка конвертации RUB->%s: %s", currency, e)
        return None
