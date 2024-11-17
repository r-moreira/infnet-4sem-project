from typing import Dict
from fastapi import APIRouter, HTTPException
from service.openai_client_service import OpenAIClientService
from model.chat_request import ChatRequest
from model.chat_response import ChatResponse
from model.spotify import TrackAudioFeaturesRequest, PlaylistAudioFeaturesRequest

class OpenAiController: 
    def __init__(self, openai_client_service: OpenAIClientService) -> None:
        self._openai_client_service = openai_client_service
        self.router = APIRouter()
        self.router.add_api_route("/chat", self.get_chat_response, methods=["POST"])
        self.router.add_api_route("/explanation/track", self.get_audio_features_explanation, methods=["POST"])
        self.router.add_api_route("/explanation/playlist", self.get_playlist_audio_features_explanation, methods=["POST"])

    async def get_chat_response(self, request: ChatRequest) -> ChatResponse:
        try:
            response = self._openai_client_service.get_chat_response(request.messages, request.api_key)
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_playlist_audio_features_explanation(self, playlist_audio_features_request: PlaylistAudioFeaturesRequest) -> ChatResponse:
        try:
            response = self._openai_client_service.get_playlist_audio_features_explanation(playlist_audio_features_request)
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_audio_features_explanation(self, track_audio_features_request: TrackAudioFeaturesRequest) -> ChatResponse:
        try:
            response = self._openai_client_service.get_audio_features_explanation(track_audio_features_request)
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))