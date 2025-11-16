from fastapi import FastAPI
from services.music import search_artist
app = FastAPI()

@app.get('/api/artists')
async def search_artist_by_name(q:str):
    return await search_artist(q)