from typing import Dict, List
from fastapi import APIRouter, HTTPException
from service.openai_client_service import OpenAIClientService
from service.local_llm_service import LocalLLMService
from model.openai_model import ChatRequest, ChatResponse
from model.spotify_model import TrackAudioFeaturesRequest, PlaylistAudioFeaturesRequest
from model.genius_model import SongLyricsInfo
import logging

class OpenAiController: 
    logger = logging.getLogger(__name__)
    
    def __init__(
            self,
            config: Dict,
            openai_client_service: OpenAIClientService,
            local_llm_service: LocalLLMService
        ) -> None:
        self._config = config
        self._openai_client_service = openai_client_service
        self._local_llm_service = local_llm_service
        self.router = APIRouter()
        self.router.add_api_route("/chat", self.get_chat_response, methods=["POST"])
        self.router.add_api_route("/explanation/track", self.get_audio_features_explanation, methods=["POST"])
        self.router.add_api_route("/explanation/playlist", self.get_playlist_audio_features_explanation, methods=["POST"])
        self.router.add_api_route("/playlist/lyrics/resume", self.get_playlist_lyrics_resume, methods=["POST"])

    async def get_chat_response(self, request: ChatRequest) -> ChatResponse:
        """
        Get chat response from OpenAI API
        
        Args:
            request (ChatRequest): Chat request
            
        Returns:
            Chat response from OpenAI API
            
        Raises:
            HTTPException: If there is an error while getting chat response
        """
        if self._config['local_llm']['enabled']:
            raise HTTPException(status_code=501, detail="Not Implemented")
        
        try:
            response = self._openai_client_service.get_chat_response(request.messages, request.api_key)
            return {"message": response}
        except Exception as e:
            self.logger.error(f"Failed to get chat response: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_playlist_lyrics_resume(self, song_lyrics_info_list: List[SongLyricsInfo]) -> ChatResponse:
        """
        Get playlist lyrics resume
        
        Args:
            song_lyrics_info_list (List[SongLyricsInfo]): List of song lyrics info
            
        Returns:
            Playlist lyrics resume
            
        Raises:
            HTTPException: If there is an error while getting playlist lyrics resume            
        """
        if self._config['local_llm']['enabled']:
            raise HTTPException(status_code=501, detail="Not Implemented")
        
        try:
            response = self._openai_client_service.get_playlist_lyrics_resume(song_lyrics_info_list)
            return {"message": response}
        except Exception as e:
            self.logger.error(f"Failed to get playlist lyrics resume: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_playlist_audio_features_explanation(self, playlist_audio_features_request: PlaylistAudioFeaturesRequest) -> ChatResponse:
        """
        Get playlist audio features explanation
        
        Args:
            playlist_audio_features_request (PlaylistAudioFeaturesRequest): Playlist audio features request
            
        Returns:
            Playlist audio features explanation
            
        Raises:
            HTTPException: If there is an error while getting playlist audio features explanation
        """
        try:            
            if self._config['local_llm']['enabled']:
                response = self._local_llm_service.get_playlist_audio_features_explanation(playlist_audio_features_request)       
            else:
                response = self._openai_client_service.get_playlist_audio_features_explanation(playlist_audio_features_request)
                
            return {"message": response}
        except Exception as e:
            self.logger.error(f"Failed to get playlist audio features explanation: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_audio_features_explanation(self, track_audio_features_request: TrackAudioFeaturesRequest) -> ChatResponse:
        """
        Get audio features explanation
        
        Args:
            track_audio_features_request (TrackAudioFeaturesRequest): Track audio features request
            
        Returns:
            Audio features explanation
            
        Raises:
            HTTPException: If there is an error while getting audio features explanation
        """
        if self._config['local_llm']['enabled']:
            raise HTTPException(status_code=501, detail="Not Implemented")
        
        try:
            response = self._openai_client_service.get_audio_features_explanation(track_audio_features_request)
            return {"message": response}
        except Exception as e:
            self.logger.error(f"Failed to get audio features explanation: {e}")
            raise HTTPException(status_code=500, detail=str(e))