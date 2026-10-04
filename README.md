# Adventure game

Text adventure with a **Python** game engine and a simple browser UI (Flask + HTML forms).

## Edit the game

Change story and logic in:

- [`game/world.py`](game/world.py) — player-facing text
- [`game/engine.py`](game/engine.py) — rooms, rules, inventory

Push to git; your host redeploys with the latest Python.

## Run locally

```bash
pip install -r requirements.txt
flask --app app run
```

Open http://127.0.0.1:5000

Or: `python app.py` (uses port 5000, or `PORT` if set).

## Terminal play (optional)

```bash
python archive/python-cli/main.py
```

## Deploy on Render

1. Create a **Web Service** at [render.com](https://render.com) and connect this repo.
2. **Runtime:** Python 3.
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
5. Deploy.

[Railway](https://railway.app) and similar hosts work the same way: install requirements, run gunicorn on `$PORT`.

## Deploy on Vercel

1. Push this repo to GitHub (or connect an existing remote).
2. At [vercel.com/new](https://vercel.com/new), import the repository.
3. Vercel detects **Flask** from `requirements.txt` and uses [`app.py`](app.py) as the entrypoint. Leave **Build Command** and **Start Command** empty (defaults are fine).
4. Deploy. Static CSS is served from [`public/static/`](public/static/).

Optional local check with the Vercel CLI: `vercel dev` (requires [Vercel CLI](https://vercel.com/docs/cli) 48.2.10+).

## Layout

```
game/              # world + engine (source of truth)
app.py             # Flask web app
templates/         # HTML
public/static/     # CSS (CDN on Vercel; Flask serves locally)
archive/python-cli/  # optional terminal entry
```
