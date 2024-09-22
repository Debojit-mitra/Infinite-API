from pydantic import BaseModel
from typing import Optional, List

class LibgenBookData(BaseModel):
    id: str
    author: str
    title: str
    publisher: str
    year: str
    pages: str
    language: str
    size: str
    extension: str
    download_id: str   # This can be None if there's no link

class DownloadLinkResponse(BaseModel):
    download_link: str

class LibgenSearchResponse(BaseModel):
    total_results: int
    books: List[LibgenBookData]