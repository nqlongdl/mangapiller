import sqlite3
import os

DB_PATH = "/app/data/manga.db"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

# Sent chapters
conn.execute("""
CREATE TABLE IF NOT EXISTS sent (
    url TEXT PRIMARY KEY,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Favorite manga
conn.execute("""
CREATE TABLE IF NOT EXISTS favorite (
    title TEXT PRIMARY KEY
)
""")
conn.commit()

# --- FAVORITE CRUD ---
def get_favorites():
    cur = conn.execute("SELECT title FROM favorite")
    return [row[0].lower() for row in cur.fetchall()]

def add_favorite(title):
    conn.execute("INSERT OR IGNORE INTO favorite(title) VALUES(?)", (title,))
    conn.commit()

def remove_favorite(title):
    conn.execute("DELETE FROM favorite WHERE LOWER(title)=LOWER(?)", (title,))
    conn.commit()

# --- Sent chapters ---
def already_sent(url):
    cur = conn.execute("SELECT 1 FROM sent WHERE url=?", (url,))
    return cur.fetchone() is not None

def mark_sent(url):
    conn.execute("INSERT OR IGNORE INTO sent(url) VALUES(?)", (url,))
    conn.commit()

def cleanup_sent():
    conn.execute("DELETE FROM sent WHERE sent_at < datetime('now', '-1 day')")
    conn.commit()