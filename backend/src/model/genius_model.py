from pydantic import BaseModel
from typing import Optional

class SongLyricsInfo(BaseModel):
    song_name: str
    artist: str
    lyrics: str