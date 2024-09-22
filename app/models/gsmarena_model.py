from pydantic import BaseModel
from typing import List, Dict

class GSMArenaPhoneData(BaseModel):
    name: str
    image_url: str
    phone_url: str

class GSMArenaSearchResponse(BaseModel):
    total_results: int
    phones: List[GSMArenaPhoneData]

class PhoneDetailsResponse(BaseModel):
    id: str
    photo_url: str
    specifications: Dict[str, Dict[str, str]]