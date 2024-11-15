from pydantic import BaseModel
from typing import List, Dict, Optional

class Image(BaseModel):
    url: str

class Owner(BaseModel):
    display_name: str

class ExternalUrls(BaseModel):
    spotify: str

class Artist(BaseModel):
    name: str

class Album(BaseModel):
    name: str

class Track(BaseModel):
    album: Album
    artists: List[Artist]
    name: str
    id: str

class TrackItem(BaseModel):
    track: Track

class Tracks(BaseModel):
    items: List[TrackItem]
    total: int

class Playlist(BaseModel):
    images: List[Image]
    owner: Owner
    external_urls: ExternalUrls
    tracks: Tracks
    name: str
    description: str
    id: str