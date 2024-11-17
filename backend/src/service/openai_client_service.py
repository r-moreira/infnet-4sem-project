import openai
from openai import OpenAI, OpenAIError
from typing import List, Dict
from model.spotify_model import TrackAudioFeaturesRequest, PlaylistAudioFeaturesRequest
import logging

class OpenAIClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class OpenAIClientService:
    logger = logging.getLogger(__name__)
    
    def __init__(self, config: Dict) -> None:
        self._api_key = config["openai"]["api_key"]
    
    def get_chat_response(self, messages: List[Dict[str, str]], api_key: str) -> str:
        if not api_key:
            raise OpenAIClientError("API Key is required.")
        
        openai.api_key = api_key
        client: OpenAI = openai
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            self.logger.error(f"Failed to get chat response: {e}")
            raise OpenAIClientError(f"Failed to get chat response: {e}")
    
    def get_playlist_audio_features_explanation(self, playlist_audio_features_request: PlaylistAudioFeaturesRequest) -> str:
        openai.api_key = self._api_key
        client: OpenAI = openai 
        
        metrics = playlist_audio_features_request.metrics
        
        prompt = f"""
        Provide a humanized explanation of the audio features of the following playlist:

        Playlist Name: {playlist_audio_features_request.name}

        Playlist Description: {playlist_audio_features_request.description}

        Audio Features:
        Mean Danceability: {metrics.mean_danceability}
        Mean Energy: {metrics.mean_energy}
        Mean Loudness: {metrics.mean_loudness}
        Mean Speechiness: {metrics.mean_speechiness}
        Mean Acousticness: {metrics.mean_acousticness}
        Mean Instrumentalness: {metrics.mean_instrumentalness}
        Mean Liveness: {metrics.mean_liveness}
        Mean Valence: {metrics.mean_valence}
        Mean Tempo: {metrics.mean_tempo}
        Mean Duration (ms): {metrics.mean_duration_ms}
        Mode Count:
        Major: {metrics.mode_count.major}
        Minor: {metrics.mode_count.minor}
        Key Count:
        C: {metrics.key_count.C}
        C#: {metrics.key_count.C_sharp}
        D: {metrics.key_count.D}
        D#: {metrics.key_count.D_sharp}
        E: {metrics.key_count.E}
        F: {metrics.key_count.F}
        F#: {metrics.key_count.F_sharp}
        G: {metrics.key_count.G}
        G#: {metrics.key_count.G_sharp}
        A: {metrics.key_count.A}
        A#: {metrics.key_count.A_sharp}
        B: {metrics.key_count.B}
        """
        
        messages = [
            {"role": "system", "content": "You are a music expert that helps people understand Spotify playlist audio features metrics."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            self.logger.error(f"Failed to get playlist audio features explanation: {e}")
            raise OpenAIClientError(f"Failed to get playlist audio features explanation: {e}")
    
    def get_audio_features_explanation(self, track_audio_features_request: TrackAudioFeaturesRequest) -> str:
        openai.api_key = self._api_key
        client: OpenAI = openai 

        audio_features = track_audio_features_request.audio_features
        
        prompt = f"""
        Provide a humanized explanation of the following Spotify audio features:

        Danceability: {audio_features.danceability}
        Energy: {audio_features.energy}
        Key: {audio_features.key}
        Loudness: {audio_features.loudness}
        Mode: {audio_features.mode}
        Speechiness: {audio_features.speechiness}
        Acousticness: {audio_features.acousticness}
        Instrumentalness: {audio_features.instrumentalness}
        Liveness: {audio_features.liveness}
        Valence: {audio_features.valence}
        Tempo: {audio_features.tempo}
        Duration (ms): {audio_features.duration_ms}
        Time Signature: {audio_features.time_signature}
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            self.logger.error(f"Failed to get audio features explanation: {e}")
            raise OpenAIClientError(f"Failed to get audio features explanation: {e}")