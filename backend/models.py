from pydantic import BaseModel
from typing import List

class ArtistProfile(BaseModel):
    name:str
    country:str
    birth_date:str
    tags:List[str]
    bio:str
    links:List[str]

