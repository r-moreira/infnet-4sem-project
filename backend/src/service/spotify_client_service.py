from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import logging
from model.spotify import Playlist, AudioFeatures, AudioFeaturesMetrics, AudioFeaturesModesCount, AudioFeaturesKeysCount, AudioFeaturesResponse
from typing import Any, Dict, List, Optional

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
    
    def get_playlist(self, url: str) -> Optional[Playlist]:
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
    
    def get_audio_features(self, track_id_list: List[str]) -> Optional[AudioFeaturesResponse]:
        self.logger.info(f"Getting track info from {track_id_list}")
        audio_features_list = self._sp.audio_features(track_id_list)  
        
        if not audio_features_list:
            return None
        
        mean_metrics = {
            "danceability": 0,
            "energy": 0,
            "loudness": 0,
            "speechiness": 0,
            "acousticness": 0,
            "instrumentalness": 0,
            "liveness": 0,
            "valence": 0,
            "tempo": 0,
            "duration_ms": 0
        }
        
        mode_count = {"major": 0, "minor": 0}
        key_count = {k: 0 for k in ["C", "C_sharp", "D", "D_sharp", "E", "F", "F_sharp", "G", "G_sharp", "A", "A_sharp", "B"]}
        
        num_songs = len(audio_features_list)
        
        for features in audio_features_list:
            mean_metrics["danceability"] += features["danceability"]
            mean_metrics["energy"] += features["energy"]
            mean_metrics["loudness"] += features["loudness"]
            mean_metrics["speechiness"] += features["speechiness"]
            mean_metrics["acousticness"] += features["acousticness"]
            mean_metrics["instrumentalness"] += features["instrumentalness"]
            mean_metrics["liveness"] += features["liveness"]
            mean_metrics["valence"] += features["valence"]
            mean_metrics["tempo"] += features["tempo"]
            mean_metrics["duration_ms"] += features["duration_ms"]
            
            mode_count["major" if features["mode"] == 1 else "minor"] += 1
            key_count[list(key_count.keys())[features["key"]]] += 1
    
        for key in mean_metrics:
            mean_metrics[key] /= num_songs
    
        audio_features_metrics = AudioFeaturesMetrics(
            mean_danceability=mean_metrics["danceability"],
            mean_energy=mean_metrics["energy"],
            mean_loudness=mean_metrics["loudness"],
            mean_speechiness=mean_metrics["speechiness"],
            mean_acousticness=mean_metrics["acousticness"],
            mean_instrumentalness=mean_metrics["instrumentalness"],
            mean_liveness=mean_metrics["liveness"],
            mean_valence=mean_metrics["valence"],
            mean_tempo=mean_metrics["tempo"],
            mean_duration_ms=mean_metrics["duration_ms"],
            mode_count=AudioFeaturesModesCount(major=mode_count["major"], minor=mode_count["minor"]),
            key_count=AudioFeaturesKeysCount(**key_count)
        )
        
        audio_features_response = AudioFeaturesResponse(
            audio_features=[AudioFeatures(
                danceability=features["danceability"],
                energy=features["energy"],
                key=features["key"],
                loudness=features["loudness"],
                mode=int(features["mode"]), 
                speechiness=features["speechiness"],
                acousticness=features["acousticness"],
                instrumentalness=features["instrumentalness"],
                liveness=features["liveness"],
                valence=features["valence"],
                tempo=features["tempo"],
                type=features.get("type"),
                id=features.get("id"),
                uri=features.get("uri"),
                track_href=features.get("track_href"),
                analysis_url=features.get("analysis_url"),
                duration_ms=features["duration_ms"],
                time_signature=int(features["time_signature"])
            ) for features in audio_features_list],
            metrics=audio_features_metrics
        )
              
        return audio_features_response