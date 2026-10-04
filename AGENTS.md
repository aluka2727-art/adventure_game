# Agent & developer guide

Text adventure: **Python game logic** + **Flask** web UI (HTML forms, no JavaScript build step).

## Repository layout

| Path | Purpose |
|------|---------|
| `game/world.py` | Story text, room copy, constants |
| `game/engine.py` | Rooms, rules, inventory, `process_turn()` |
| `app.py` | Flask routes; calls `process_turn` only |
| `templates/`, `static/` | Web UI |
| `requirements.txt` | Runtime dependencies (`flask`, `gunicorn`) |
| `archive/python-cli/` | Optional terminal entry (`main.py`) |
| `archive/web-react/` | Old React UI (reference only; not used) |

**Source of truth for gameplay:** `game/`. The web layer should stay thin.

## Python environment (recommended: uv)

Use a **project-local** virtual environment at `.venv/` (already gitignored). Do not install project packages globally.

### Install uv (once per machine)

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or see [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/).

### First-time setup

From the repository root:

```bash
cd /path/to/adventure_game
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Day-to-day

```bash
source .venv/bin/activate
# edit code, run commands below
```

After adding a dependency:

```bash
uv pip install <package>
uv pip freeze > requirements.txt   # only if the new package should be committed
```

### Without uv (stdlib venv + pip)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the web app locally

With the venv activated:

```bash
flask --app app run
```

Open **http://127.0.0.1:5000**

Alternatives:

```bash
python app.py              # PORT env var supported (default 5000)
flask --app app run --debug   # auto-reload while developing
```

Production-style check (optional):

```bash
gunicorn --bind 127.0.0.1:5000 app:app
```

## Run in the terminal (no browser)

```bash
python archive/python-cli/main.py
```

## Deploy

Hosts such as Render or Railway:

- **Build:** `pip install -r requirements.txt` (or `uv pip install -r requirements.txt` in CI)
- **Start:** `gunicorn --bind 0.0.0.0:$PORT app:app`

See `render.yaml` and `README.md` for a Render blueprint.

## Conventions for agents

1. **Gameplay changes** → `game/world.py` and/or `game/engine.py`. Avoid duplicating rules in `app.py`.
2. **UI changes** → `templates/play.html`, `static/style.css`, and only as much `app.py` as needed for rendering.
3. **No npm / React** for the live app unless the user explicitly revives `archive/web-react/`.
4. **Keep diffs small**; match existing style in `game/` and Flask code.
5. **Do not commit** `.venv/`, `__pycache__/`, or secrets.
6. **Tests / smoke checks:** Flask test client on `app`, or `curl` against `/` after `flask --app app run`.

## Quick mental model

```text
Browser form POST → app.py → process_turn(state, command) → HTML page
```

Game state is carried in hidden form fields (JSON), not server sessions.
