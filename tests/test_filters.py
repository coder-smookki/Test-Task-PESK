from unittest.mock import MagicMock

import pytest

from app.bot.filters.city_input import CityInputFilter


@pytest.fixture
def f():
    return CityInputFilter()


def _msg(text):
    m = MagicMock()
    m.text = text
    return m


async def test_valid_integer_amount(f):
    result = await f(_msg("Москва, 1000"))
    assert result == {"city": "Москва", "amount": 1000.0}


async def test_valid_float_dot(f):
    result = await f(_msg("Берлин, 1500.50"))
    assert result == {"city": "Берлин", "amount": 1500.5}


async def test_valid_float_comma(f):
    result = await f(_msg("Берлин, 1500,50"))
    assert result == {"city": "Берлин", "amount": 1500.5}


async def test_no_separator_rejected(f):
    assert await f(_msg("Москва 1000")) is False


async def test_empty_text_rejected(f):
    m = MagicMock()
    m.text = None
    assert await f(m) is False


async def test_zero_amount_rejected(f):
    assert await f(_msg("Москва, 0")) is False


async def test_strips_whitespace(f):
    result = await f(_msg("  Токио  ,  500  "))
    assert result == {"city": "Токио", "amount": 500.0}
