import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class CityInputFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict:
        if not message.text:
            return False
        match = re.match(r"^(.+?),\s*(\d+)$", message.text.strip())
        if not match:
            return False
        return {"city": match.group(1).strip(), "amount": int(match.group(2))}
