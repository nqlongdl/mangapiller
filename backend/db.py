import sqlite3
import os

DB_PATH = "/app/manga.db"

if not os.path.exists(DB_PATH):
    open(DB_PATH, "w").close()

conn = sqlite3.connect("/app/manga.db", check_same_thread=False)

# Sent chapters
conn.execute("""
CREATE TABLE IF NOT EXISTS sent (
    url TEXT PRIMARY KEY
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