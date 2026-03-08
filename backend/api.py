from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import db
import os

app = FastAPI()

class FavoriteItem(BaseModel):
    title: str

@app.get("/api/favorites")
def list_favorites():
    return db.get_favorites()

@app.post("/api/favorites")
def add_favorite(item: FavoriteItem):
    db.add_favorite(item.title)
    return {"added": item.title}

@app.delete("/api/favorites")
def remove_favorite(item: FavoriteItem):
    db.remove_favorite(item.title)
    return {"removed": item.title}

FRONTEND_DIR = "/app/frontend/dist"
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")