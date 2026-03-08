from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import HTTPException
import asyncio
import db
import os
import logger

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

@app.post("/api/check")
def trigger_check():
    import sys
    main = sys.modules.get('__main__')
    if main is None or not main.bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot not ready yet.")
    future = asyncio.run_coroutine_threadsafe(main.do_check(), main.bot.loop)
    try:
        found = future.result(timeout=30)
        return {"found": found}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

FRONTEND_DIR = "/app/frontend/dist"
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")