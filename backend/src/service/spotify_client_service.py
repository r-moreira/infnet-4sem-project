from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
from model.spotify import Playlist
from typing import Any, Dict, List

class SpotifyClientService:
    def __init__(self, config: Dict) -> None:
        self._client_credentials_manager = SpotifyClientCredentials(
            client_id=config["spotify"]["client_id"],
            client_secret=config["spotify"]["client_secret"]
        )
        self._sp = spotipy.Spotify(client_credentials_manager=self._client_credentials_manager)
        
    
    def search(self, query: str) -> Any | None:
        results = self._sp.search(q=query, limit=20)
        return results
    
    def get_playlist(self, url: str) -> Playlist | None:
        fields = ','.join([
            'id',
            'name',
            'owner.display_name',
            'description',
            'external_urls',
            'images.url',
            'tracks.total',
            'tracks.items.track.id',
            'tracks.items.track.name',
            'tracks.items.track.artists.name',
            'tracks.items.track.album.name'
        ])
        
        playlist = self._sp.playlist(url, fields=fields)
        return playlist