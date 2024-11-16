from typing import List
from enum import Enum

class ViewStrategy(Enum):
    HOME = "Home"
    # ALBUM_ANALYSIS = "Album Analysis (Beta)"
    # SONG_ANALYSIS = "Song Analysis (Beta)"
    # CHAT = "Chat (Beta)"
    PLAYLIST = "Playlist Analysis"
    
    @staticmethod
    def to_value_list() -> List:
        return [e.value for e in ViewStrategy]