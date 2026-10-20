# Personal page

Based on [Martin Saveski's Jekyll template](https://github.com/msaveski/www_personal).

## Edit content
- `_data/main_info.yaml` – name, title, email, links, profile picture
- `_data/publications.yaml` – publications (thumbnail images go in `assets/publications/`)
- `_data/education.yaml` – education
- `index.html` – About text and section layout

## Local preview (no Ruby/Jekyll needed)
```
_preview/venv/bin/python _preview/render.py      # renders to _site/
python3 -m http.server -d _site 8765             # open http://localhost:8765/
```
To (re)create the venv: `python3 -m venv _preview/venv && _preview/venv/bin/pip install python-liquid pyyaml`.

GitHub Pages builds the Jekyll sources directly, so `_site/` is not committed.
