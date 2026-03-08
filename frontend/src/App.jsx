import React, { useState, useEffect } from "react";
import "./App.css";

export default function App() {
  const [favorites, setFavorites] = useState([]);
  const [newTitle, setNewTitle] = useState("");

  const [toast, setToast] = useState(null);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

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

  const [checking, setChecking] = useState(false);
  const triggerCheck = async () => {
    setChecking(true);
    try {
      const res = await fetch("/api/check", { method: "POST" });
      if (res.status === 503) {
        showToast("⏳ Bot is starting up, try again in a few seconds.");
        return;
      }
      const data = await res.json();
      if (!res.ok) {
        showToast(`❌ Error: ${data.detail}`);
        return;
      }
      showToast(data.found > 0 ? `✅ Found ${data.found} new chapter(s)!` : "😴 No new chapters today.");
    } catch (e) {
      showToast("❌ Failed to connect to server.");
    } finally {
      setChecking(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") addFavorite();
  };

  useEffect(() => { fetchFavorites(); }, []);

  return (
    <>
      <div className="app">
       <div className="header">
        <div>
          <div className="header-label">MangaPill Notifier</div>
          <h1>WATCH<br /><span>LIST</span></h1>
        </div>
        <a href="https://mangapill.com" target="_blank" rel="noopener noreferrer" style={{ textDecoration: "none" }}>
          <button className="btn-visit">Browse MangaPill</button>
        </a>
      </div>

        <div className="input-row">
          <input
            value={newTitle}
            onChange={e => setNewTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter manga title..."
          />
          <button className="btn-add" onClick={addFavorite}>ADD</button>
          <button className="btn-visit" onClick={triggerCheck} disabled={checking}>
            {checking ? "Checking..." : "Check Now 🔔"}
          </button>
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
      {toast && <div className="toast">{toast}</div>}
    </>
  );
}