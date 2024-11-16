import openai
from openai import OpenAI, OpenAIError, ChatCompletion
from typing import List, Dict
from model.spotify import AudioFeatures

class OpenAIClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class OpenAIClientService:
    def __init__(self, config: Dict) -> None:
        self._api_key = config["openai"]["api_key"]
    
    def get_chat_response(self, messages: List[Dict[str, str]], api_key: str) -> str:
        if not api_key:
            raise OpenAIClientError("API Key is required.")
        
        openai.api_key = api_key
        client: OpenAI = openai
        
        try:
            response: ChatCompletion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            raise OpenAIClientError(f"An error occurred: {e}")
        
    def get_audio_features_explanation(self, audio_features: AudioFeatures) -> str:
        openai.api_key = self._api_key
        client: OpenAI = openai 
        
        prompt = (
            "Provide a humanized explanation of the following Spotify audio features:\n\n"
            f"Danceability: {audio_features.danceability}\n"
            f"Energy: {audio_features.energy}\n"
            f"Key: {audio_features.key}\n"
            f"Loudness: {audio_features.loudness}\n"
            f"Mode: {audio_features.mode}\n"
            f"Speechiness: {audio_features.speechiness}\n"
            f"Acousticness: {audio_features.acousticness}\n"
            f"Instrumentalness: {audio_features.instrumentalness}\n"
            f"Liveness: {audio_features.liveness}\n"
            f"Valence: {audio_features.valence}\n"
            f"Tempo: {audio_features.tempo}\n"
            f"Duration (ms): {audio_features.duration_ms}\n"
            f"Time Signature: {audio_features.time_signature}\n"
        )
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response: ChatCompletion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            
            raise OpenAIClientError(f"An error occurred: {e}")