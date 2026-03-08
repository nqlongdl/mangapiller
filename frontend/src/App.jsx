import React, { useState, useEffect } from "react";

export default function App() {
  const [favorites, setFavorites] = useState([]);
  const [newTitle, setNewTitle] = useState("");

  const fetchFavorites = async () => {
    const res = await fetch("/api/favorites");
    setFavorites(await res.json());
  };

  const addFavorite = async () => {
    if (!newTitle) return;
    await fetch("/api/favorites", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle }),
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

  useEffect(() => { fetchFavorites(); }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Favorite Manga</h2>
      <input value={newTitle} onChange={e => setNewTitle(e.target.value)} placeholder="Add title" />
      <button onClick={addFavorite}>Add</button>
      <ul>
        {favorites.map(f => (
          <li key={f}>
            {f} <button onClick={() => removeFavorite(f)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}