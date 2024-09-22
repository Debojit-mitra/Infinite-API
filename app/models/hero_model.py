from pydantic import BaseModel
from typing import List, Dict
from typing import Optional

class HeroData(BaseModel):
    hero_id: str
    name: str
    image_url: str

class HeroSearchResponse(BaseModel):
    heroes: List[HeroData]

class GalleryImage(BaseModel):
    url: str
    caption: str

class HeroDetail(BaseModel):
    hero_id: str
    name: str
    image_url: str
    details: Dict[str, str]
    biography: str
    gallery: List[GalleryImage]
    
class HeroSearchResult(BaseModel):
    name: str
    hero_id: str
    thumbnail: str
    description: str

class HeroSearchResponse(BaseModel):
    total_results: int
    results: List[HeroSearchResult]