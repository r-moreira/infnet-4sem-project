from transformers import pipeline
import torch
from model.local_llm_model import ChatResponse
from model.spotify_model import PlaylistAudioFeaturesRequest
import logging
from typing import Dict

class LocalLLMService:
    logger = logging.getLogger(__name__)
    
    def __init__(self, config: Dict) -> None:
        self._config = config
     
    def get_playlist_audio_features_explanation(self, playlist_audio_features_request: PlaylistAudioFeaturesRequest) -> ChatResponse:
        self.logger.info("Getting playlist audio features explanation.")
        
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
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            device=device, 
            max_length=int(self._config['local_llm']['max_length']),
            torch_dtype=torch.bfloat16
        )
        
        prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = pipe(prompt, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        generated_text = outputs[0]['generated_text']       
        assistant_response = generated_text.split('<|assistant|>')[-1].split('</s>')[0].strip()

        return assistant_response