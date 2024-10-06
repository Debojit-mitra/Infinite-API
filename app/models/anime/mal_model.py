from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MalDataType1(BaseModel):
    rank: str
    title: str
    url: str
    image_small_url: str
    image_url: str
    score: str

class MalResponseType1(BaseModel):
    page: int
    total_results_here: int
    total_pages: int
    results: List[MalDataType1]

class AnimeSeasonAndScheduleData(BaseModel):
    url: str
    title: str
    image_url: str
    score: str
    adult: bool
    genres: List[str]
    synopsis: str

class AnimeSeasonAndScheduleResponse(BaseModel):
    total_results: int
    year: int
    season: str
    results: Dict[str, List[AnimeSeasonAndScheduleData]]

class AnimeSearchResult(BaseModel):
    title: str = ''
    url: str = ''
    image_small: str = ''
    image_large: str = ''
    type: str = ''
    episodes: str = ''
    score: str = ''
    synopsis: str = ''
    

class AnimeSearchResponse(BaseModel):
    page: int
    total_pages: int
    results: List[AnimeSearchResult]

#anime details
class StreamingPlatform(BaseModel):
    name: str
    icon: Optional[str]
    url: Optional[str]

class RelatedAnime(BaseModel):
    title: str
    url: str
    type: str
    image_url: str

class VoiceActor(BaseModel):
    name: str
    image_url: str
    language: str

class Character(BaseModel):
    name: str
    url: str
    image_url: str
    role: str
    voice_actors: List[VoiceActor]

class Theme(BaseModel):
    number: str
    title: str
    artist: str
    episodes: Optional[str]
    platforms: Dict[str, str]

class Recommendation(BaseModel):
    title: str
    url: str
    image_url: str
    recommenders: str

class AnimeDetails(BaseModel):
    title: str
    english_title: Optional[str]
    type: str
    episodes: str
    status: str
    aired: str
    premiered: str
    broadcast: str
    producers: Dict[str, str]
    licensors: List[str]
    studios: Dict[str, str]
    source: str
    genres: List[str]
    themes: List[str]
    demographics: List[str]
    duration: str
    rating: str
    score: str
    ranked: str
    popularity: str
    synopsis: str
    related_entries: Dict[str, List[RelatedAnime]]
    characters: List[Character]
    themes: Dict[str, List[Theme]]
    recommendations: List[Recommendation]

# anime character details
class VoiceActor(BaseModel):
    name: str
    language: str
    url: Optional[str]
    image_url: Optional[str]

class CharacterDetails(BaseModel):
    name: str
    image_url: Optional[str]
    details: str
    spoiler: Optional[str]
    voice_actors: List[VoiceActor]

# people details
class VoiceActingRole(BaseModel):
    anime_name: str
    anime_url: Optional[str]
    anime_image: Optional[str]
    character_name: str
    character_url: Optional[str]
    character_image: Optional[str]
    role: str

class AnimeStaffPosition(BaseModel):
    anime: str
    anime_url: Optional[str]
    anime_image: Optional[str]
    position: str

class PersonDetails(BaseModel):
    name: str
    image_url: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    alternate_names: List[str]
    birthday: Optional[str]
    about: Dict[str, Any]
    voice_acting_roles: List[VoiceActingRole]
    anime_staff_positions: List[AnimeStaffPosition]