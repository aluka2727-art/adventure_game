import { useCallback, useEffect, useRef, useState } from "react";

const API_URL = "/api/play";

function formatInventory(items) {
  if (!items?.length) {
    return "Inventory: (empty)";
  }
  return `Inventory: ${items.join(", ")}`;
}

async function callPlay(state, input) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state, input }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `Request failed (${res.status})`);
  }
  return res.json();
}

export default function App() {
  const [lines, setLines] = useState([]);
  const [gameState, setGameState] = useState(null);
  const [input, setInput] = useState("");
  const [inventory, setInventory] = useState([]);
  const [ended, setEnded] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const logRef = useRef(null);
  const inputRef = useRef(null);

  const applyResult = useCallback((result) => {
    setGameState(result.state);
    setInventory(result.inventory || []);
    setEnded(result.ended);
    setGameOver(
      result.ended &&
        result.messages?.some((m) => m.includes("GAME OVER")),
    );
    if (result.messages?.length) {
      setLines((prev) => [
        ...prev,
        ...result.messages.map((text) => ({ text, className: "line" })),
      ]);
    }
    if (result.prompt) {
      setLines((prev) => [
        ...prev,
        { text: result.prompt, className: "line prompt" },
      ]);
    }
  }, []);

  const startSession = useCallback(async () => {
    setLines([]);
    setGameState(null);
    setInput("");
    setInventory([]);
    setEnded(false);
    setGameOver(false);
    setError(null);
    setLoading(true);
    try {
      const result = await callPlay(null, null);
      applyResult(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [applyResult]);

  useEffect(() => {
    startSession();
  }, [startSession]);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [lines]);

  useEffect(() => {
    if (!ended && !loading) {
      inputRef.current?.focus();
    }
  }, [ended, loading, lines]);

  async function handleSubmit(e) {
    e.preventDefault();
    const value = input.trim();
    if (!value || ended || loading || !gameState) {
      return;
    }
    setInput("");
    setLines((prev) => [...prev, { text: `> ${value}`, className: "line" }]);
    setLoading(true);
    setError(null);
    try {
      const result = await callPlay(gameState, value);
      applyResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Adventure</h1>
        <p>
          Work in progress — game logic runs on Python. Type answers as prompts
          suggest (yes, left, fight).
        </p>
      </header>

      {error && <p className="error-banner">{error}</p>}

      <div className="terminal">
        <div
          className="log"
          ref={logRef}
          aria-live="polite"
          aria-relevant="additions"
        >
          {lines.map((line, i) => (
            <div
              key={i}
              className={`${line.className}${gameOver && line.className === "line" && line.text.includes("GAME OVER") ? " game-over" : ""}`}
            >
              {line.text}
            </div>
          ))}
        </div>
        <div className="inventory">{formatInventory(inventory)}</div>
        <form className="input-row" onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={ended || loading}
            placeholder={
              loading ? "…" : ended ? "Game ended" : "Your answer…"
            }
            autoComplete="off"
            spellCheck={false}
            aria-label="Game input"
          />
          <button type="submit" disabled={ended || loading || !input.trim()}>
            Send
          </button>
        </form>
      </div>

      <div className="actions">
        <button type="button" onClick={startSession} disabled={loading}>
          New game
        </button>
      </div>
    </div>
  );
}
