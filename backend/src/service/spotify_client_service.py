from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import logging
from model.spotify import Playlist, AudioFeatures
from typing import Any, Dict, List

class SpotifyClientService:
    logger = logging.getLogger(__name__)
        
    def __init__(self, config: Dict) -> None:
        self._client_credentials_manager = SpotifyClientCredentials(
            client_id=config["spotify"]["client_id"],
            client_secret=config["spotify"]["client_secret"]
        )
        self._sp = spotipy.Spotify(client_credentials_manager=self._client_credentials_manager)
        
    
    def search(self, query: str) -> Any | None:
        self.logger.info(f"Searching for {query}")
        results = self._sp.search(q=query, limit=20)
        return results
    
    def get_playlist(self, url: str) -> Playlist | None:
        self.logger.info(f"Getting playlist from {url}")
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
    
    def get_audio_features(self, track_id_list: List[str]) -> List[AudioFeatures] | None:
        self.logger.info(f"Getting track info from {track_id_list}")
        track = self._sp.audio_features(track_id_list)
        return track