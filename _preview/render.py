"""Minimal local renderer for this Jekyll site (no Ruby needed).

Renders index.html through _layouts/default.html with python-liquid,
using _data/*.yaml and _config.yml, and copies libs/ and assets/ to _site/.
"""
import re
import shutil
from pathlib import Path

import yaml
from liquid import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

config = yaml.safe_load((ROOT / "_config.yml").read_text()) or {}
data = {p.stem: yaml.safe_load(p.read_text()) for p in (ROOT / "_data").glob("*.yaml")}
site = {"baseurl": config.get("baseurl", "") or "", "data": data}

env = Environment(loader=FileSystemLoader(ROOT / "_includes"))

FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
INCLUDE = re.compile(r"{%-?\s*include\s+([\w./-]+)\s*-?%}")


def inline_includes(text: str) -> str:
    """Jekyll's `{% include file.html %}` takes a bare filename; inline it."""
    return INCLUDE.sub(lambda m: (ROOT / "_includes" / m.group(1)).read_text(), text)


def render_page(src: Path, dst: Path):
    text = src.read_text()
    m = FM.match(text)
    page = yaml.safe_load(m.group(1)) or {} if m else {}
    body = text[m.end():] if m else text
    content = env.from_string(inline_includes(body)).render(site=site, page=page)
    layout = page.get("layout")
    if layout:
        layout_src = (ROOT / "_layouts" / f"{layout}.html").read_text()
        content = env.from_string(inline_includes(layout_src)).render(site=site, page=page, content=content)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content)


if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for d in ("libs", "assets"):
    if (ROOT / d).exists():
        shutil.copytree(ROOT / d, OUT / d)
render_page(ROOT / "index.html", OUT / "index.html")
print(f"rendered -> {OUT}")
