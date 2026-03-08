import React, { useState, useEffect } from "react";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: #0a0a0a;
    color: #f0ede8;
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
  }

  .app {
    max-width: 560px;
    margin: 0 auto;
    padding: 60px 24px;
  }

  .header {
    margin-bottom: 48px;
  }

  .header-label {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff6b2b;
    font-weight: 500;
    margin-bottom: 8px;
  }

  .header h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 64px;
    line-height: 0.9;
    color: #f0ede8;
    letter-spacing: 0.02em;
  }

  .header h1 span {
    color: #ff6b2b;
  }

  .input-row {
    display: flex;
    gap: 10px;
    margin-bottom: 40px;
  }

  .input-row input {
    flex: 1;
    background: #161616;
    border: 1px solid #2a2a2a;
    color: #f0ede8;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    padding: 14px 18px;
    outline: none;
    border-radius: 4px;
    transition: border-color 0.2s;
  }

  .input-row input::placeholder { color: #444; }
  .input-row input:focus { border-color: #ff6b2b; }

  .btn-add {
    background: #ff6b2b;
    color: #0a0a0a;
    border: none;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 18px;
    letter-spacing: 0.05em;
    padding: 14px 24px;
    cursor: pointer;
    border-radius: 4px;
    transition: background 0.2s, transform 0.1s;
    white-space: nowrap;
  }

  .btn-add:hover { background: #ff8c55; }
  .btn-add:active { transform: scale(0.97); }

  .section-label {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #444;
    font-weight: 500;
    margin-bottom: 16px;
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 18px;
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 4px;
    transition: border-color 0.2s, background 0.2s;
    animation: slideIn 0.25s ease;
  }

  @keyframes slideIn {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .item:hover { background: #161616; border-color: #2a2a2a; }

  .item-index {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 13px;
    color: #333;
    min-width: 28px;
  }

  .item-title {
    flex: 1;
    font-size: 14px;
    font-weight: 400;
    color: #c8c4be;
    text-transform: capitalize;
    letter-spacing: 0.01em;
  }

  .btn-remove {
    background: none;
    border: 1px solid #2a2a2a;
    color: #555;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    padding: 5px 12px;
    cursor: pointer;
    border-radius: 3px;
    transition: all 0.2s;
    letter-spacing: 0.03em;
  }

  .btn-remove:hover { border-color: #ff6b2b; color: #ff6b2b; background: rgba(255,107,43,0.06); }

  .empty {
    text-align: center;
    padding: 48px 0;
    color: #333;
    font-size: 13px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  .count {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 13px;
    color: #ff6b2b;
    margin-left: 8px;
  }
`;

export default function App() {
  const [favorites, setFavorites] = useState([]);
  const [newTitle, setNewTitle] = useState("");

  const fetchFavorites = async () => {
    const res = await fetch("/api/favorites");
    setFavorites(await res.json());
  };

  const addFavorite = async () => {
    if (!newTitle.trim()) return;
    await fetch("/api/favorites", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle.trim() }),
    });
    setNewTitle("");
    fetchFavorites();
  };

  const removeFavorite = async (title) => {
    await fetch("/api/favorites", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    fetchFavorites();
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") addFavorite();
  };

  useEffect(() => { fetchFavorites(); }, []);

  return (
    <>
      <style>{styles}</style>
      <div className="app">
        <div className="header">
          <div className="header-label">MangaPill Notifier</div>
          <h1>WATCH<br /><span>LIST</span></h1>
        </div>

        <div className="input-row">
          <input
            value={newTitle}
            onChange={e => setNewTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter manga title..."
          />
          <button className="btn-add" onClick={addFavorite}>ADD</button>
        </div>

        <div className="section-label">
          Tracking
          {favorites.length > 0 && <span className="count">{favorites.length}</span>}
        </div>

        <div className="list">
          {favorites.length === 0 ? (
            <div className="empty">No manga added yet</div>
          ) : (
            favorites.map((f, i) => (
              <div className="item" key={f}>
                <span className="item-index">#{String(i + 1).padStart(2, "0")}</span>
                <span className="item-title">{f}</span>
                <button className="btn-remove" onClick={() => removeFavorite(f)}>Remove</button>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}