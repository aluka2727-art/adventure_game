"""Run the terminal version: python archive/python-cli/main.py (from repo root)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from game.engine import play_game

if __name__ == "__main__":
    play_game()
