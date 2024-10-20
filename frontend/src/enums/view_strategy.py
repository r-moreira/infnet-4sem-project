from typing import List
from enum import Enum

class ViewStrategy(Enum):
    ALBUM_ANALYSIS = "Album Analysis (Beta)"
    SONG_ANALYSIS = "Song Analysis (Beta)"
    CHAT = "Chat (Beta)"
    
    @staticmethod
    def to_value_list() -> List:
        return [e.value for e in ViewStrategy]