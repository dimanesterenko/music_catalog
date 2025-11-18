import httpx


MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2"

HEADERS = {
    "User-Agent": "MyMusicCatalog/1.0 (dimanester8@gmail.com)"
}


async def search_artist(query:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/artist",
            params={"query": query, "fmt": "json"},
            headers=HEADERS
        )
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
        return response.json()
    

async def get_artist_releases(artist_id:int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/artist",
            params={"artist_id": artist_id, "fmt": "json"},
            headers=HEADERS
        )
        
        return response.json()