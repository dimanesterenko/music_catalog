import httpx
from fastapi import HTTPException
from models import ArtistProfile


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
    

async def fetch_wikipedia_summary(title: str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json().get("extract")
    except:
        return None

def extract_socials(relations):
    socials = {
        "wikipedia": None,
        "spotify": None,
        "youtube": None,
        "instagram": None,
        "official_site": None
    }

    for rel in relations:
        url = rel.get("url", {}).get("resource", "")

        if rel.get("type") == "wikipedia":
            socials["wikipedia"] = url

        if rel.get("type") == "official homepage":
            socials["official_site"] = url

        if "spotify.com" in url:
            socials["spotify"] = url

        if "youtube.com" in url:
            socials["youtube"] = url

        if "instagram.com" in url:
            socials["instagram"] = url

    return socials

async def get_artist_details(artist_id: str) -> ArtistProfile:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MUSICBRAINZ_URL}/artist/{artist_id}",
            params={"fmt": "json", "inc": "aliases+tags+url-rels"},
            headers=HEADERS
        )
        data = response.json()

    name = data.get("name", "")
    country = data.get("country", "")
    birth_date = data.get("life-span", {}).get("begin") or ""

    tags = [tag["name"] for tag in data.get("tags", [])]

    relations = data.get("relations", [])
    socials = extract_socials(relations)

    links_list = [url for url in socials.values() if url]

    bio = ""
    if socials.get("wikipedia"):
        title = socials["wikipedia"].split("/")[-1].replace(" ", "_")
        summary = await fetch_wikipedia_summary(title)
        bio = summary or ""

    return ArtistProfile(
        name=name,
        country=country,
        birth_date=birth_date,
        tags=tags,
        bio=bio,
        links=links_list
    )

