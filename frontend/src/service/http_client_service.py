import os
import logging
from typing import List, Dict
import streamlit as st
import requests
from urllib.parse import urlencode

class HttpClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    

class HttpClientService:            
    logger = logging.getLogger(__name__)
    
    def __init__(self):
        self._url = os.environ.get('BACKEND_URL', 'http://localhost:8000')
    
    def get_chat_response(self, messages: List[Dict[str, str]], api_key: str) -> str:    
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "api_key": api_key,
            "messages": messages
        }
        
        self.logger.info(f"Sending chat request to {self._url}/chat")
        
        response = requests.post(f"{self._url}/chat", headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["message"]
        else:
            HttpClientService.logger.error(f"Failed to get chat response: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get chat response")
        
    def get_genius_search(self, query: str) -> Dict:
        encoded_query = urlencode({"query": query})
        url = f"{self._url}/genius/search?{encoded_query}"
        
        self.logger.info(f"Sending genius search request to {url}")
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            HttpClientService.logger.error(f"Failed to get genius search: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get genius search")
        
    def get_playlist(self, url: str) -> Dict:
        url = f"{self._url}/spotify/playlist?url={url}"
        
        self.logger.info(f"Sending playlist request to {url}")
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Failed to get playlist: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get playlist")
        
    def get_audio_features(self, track_ids: List[str]) -> List[Dict]:
        url = f"{self._url}/spotify/audio-features"
        
        self.logger.info(f"Sending audio features requests to {url}")
        
        response = requests.post(url=url, json={"track_ids": track_ids})
        
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Failed to get audio features: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get audio features")
        
    def get_playlist_audio_features_explanation(
            self,
            playlist_name: str, 
            playlist_description: str, 
            audio_features: List[Dict]
        ) -> str:        
        self.logger.info(f"Sending playlist audio features explanation request to {self._url}/explanation/playlist")
        
        response = requests.post(f"{self._url}/explanation/playlist", json={
            "name": playlist_name,
            "description": playlist_description,
            "metrics": audio_features
        })
        
        if response.status_code == 200:
            return response.json()["message"]
        else:
            self.logger.error(f"Failed to get playlist audio features explanation: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get playlist audio features explanation")
        
    def get_song_lyrics(self, song_name: str, artist: str) -> Dict:
        encoded_query = urlencode({"song_name": song_name, "artist": artist})
        url = f"{self._url}/genius/lyrics?{encoded_query}"
        
        self.logger.info(f"Sending song lyrics request to {url}")
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            HttpClientService.logger.error(f"Failed to get song lyrics: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get song lyrics")