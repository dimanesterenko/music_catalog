from fastapi import FastAPI, HTTPException
from services.music import (search_artists,
                            get_artist_releases,
                            get_artist_details,
                            get_artist_bio,)

import logging
from models import ArtistProfile


app = FastAPI()

@app.get('/api/artists')
async def search_artist_by_name(q:str):
    return await search_artists(q)

@app.get('/api/artist/{artist_id}/releases')
async def releases(artist_id:str):
    return await get_artist_releases(artist_id)

@app.get("/api/artist/{artist_id}/details", response_model=ArtistProfile)
async def artist_details(artist_id: str):
    return await get_artist_details(artist_id)
