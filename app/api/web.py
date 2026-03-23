from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

_TEMPLATES = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES))

router = APIRouter(include_in_schema=False)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"static_base": "/static"})
