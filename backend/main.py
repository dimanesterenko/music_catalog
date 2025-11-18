from fastapi import FastAPI
from services.music import search_artists,get_artist_releases
app = FastAPI()

@app.get('/api/artists')
async def search_artist_by_name(q:str):
    return await search_artists(q)

@app.get('/api/artist/{artist_id}/releases')
async def releases(artist_id:str):
    return await get_artist_releases(artist_id)