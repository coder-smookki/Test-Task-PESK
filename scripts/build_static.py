import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
API_BASE = os.getenv("API_BASE_URL", "")
REPO_NAME = os.getenv("REPO_NAME", "")

static_base = f"/{REPO_NAME}/static" if REPO_NAME else "static"

env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))
template = env.get_template("index.html")
html = template.render(static_base=static_base)

if API_BASE:
    inject = f'<script>window.API_BASE = "{API_BASE}";</script>'
    html = html.replace("</body>", f"{inject}\n</body>")

dist = ROOT / "dist"
if dist.exists():
    shutil.rmtree(dist)
dist.mkdir()

(dist / "index.html").write_text(html, encoding="utf-8")

static_dst = dist / "static"
shutil.copytree(ROOT / "app" / "static", static_dst)

print(f"Built → {dist}/")
print(f"  static_base = {static_base!r}")
print(f"  API_BASE    = {API_BASE!r}")
