import httpx


MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2"

HEADERS = {
    "User-Agent": "MyMusicCatalog/1.0 (dimanester8@gmail.com)"
}


async def search_artists(query:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/artist",
            params={"query": query, "fmt": "json"},
            headers=HEADERS
        )
        # print("STATUS:", response.status_code)
        # print("BODY:", response.text)
        return response.json()
    
async def get_artist_releases(artist_mbid: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/release/",
            params={
                "artist": artist_mbid,   # MBID артиста
                "fmt": "json",
                "limit": 100
            },
            headers=HEADERS
        )
        return response.json()
