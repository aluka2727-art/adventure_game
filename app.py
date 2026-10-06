"""Web UI for the adventure game (Flask + HTML forms)."""

import json
import os

from flask import Flask, redirect, render_template, request, url_for

from game.engine import process_turn

app = Flask(__name__, static_folder="public/static")


def _append_result(log, result):
    for text in result.get("messages") or []:
        kind = "game-over" if "GAME OVER" in text else "line"
        log.append({"text": text, "kind": kind})
    prompt = result.get("prompt")
    if prompt:
        log.append({"text": prompt, "kind": "prompt"})
    return log


def _new_session():
    result = process_turn(None, None)
    log = _append_result([], result)
    return result, log


def _parse_json_field(name, default):
    raw = request.form.get(name, "")
    if not raw:
        return default
    return json.loads(raw)


@app.get("/")
def index():
    result, log = _new_session()
    return render_template(
        "play.html",
        log=log,
        state=result["state"],
        ended=result.get("ended", False),
        died=bool(result["state"].get("ended")),
        animate_from=0,
        error=None,
    )


@app.get("/new")
def new_game():
    return redirect(url_for("index"))


@app.post("/")
def play():
    try:
        state = _parse_json_field("state", None)
        log = _parse_json_field("log", [])
        command = (request.form.get("command") or "").strip()

        if state is None:
            result, log = _new_session()
            animate_from = 0
        elif not command:
            animate_from = len(log)
            result = process_turn(state, "")
            log = _append_result(log, result)
        else:
            log.append({"text": f"> {command}", "kind": "input"})
            animate_from = len(log)
            result = process_turn(state, command)
            log = _append_result(log, result)

        return render_template(
            "play.html",
            log=log,
            state=result["state"],
            ended=result.get("ended", False),
            died=bool(result["state"].get("ended")),
            animate_from=animate_from,
            error=None,
        )
    except (json.JSONDecodeError, TypeError, KeyError) as exc:
        result, log = _new_session()
        return render_template(
            "play.html",
            log=log,
            state=result["state"],
            ended=result.get("ended", False),
            died=bool(result["state"].get("ended")),
            animate_from=0,
            error=f"Something went wrong ({exc}). Started a new game.",
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
