from fastapi import APIRouter, HTTPException, Query, Body
from service.spotify_client_service import SpotifyClientService
from typing import Dict, List, Any
from model.spotify_model import Playlist, TrackIdsRequest, AudioFeaturesResponse
import logging

class SpotifyController:
    logger = logging.getLogger(__name__)
    
    def __init__(self, spotify_client_service: SpotifyClientService) -> None:
        self._spotify_client_service = spotify_client_service
        self.router = APIRouter(prefix="/spotify")
        self.router.add_api_route("/playlist", self.get_playlist, methods=["GET"])
        self.router.add_api_route(
            path="/audio-features",
            endpoint=self.get_audio_features, 
            methods=["POST"],
            response_model_exclude_none=True, 
            response_model_exclude_unset=True
        )
  
    async def get_playlist(self, url: str = Query(...)) -> Playlist:
        try:
            return self._spotify_client_service.get_playlist(url)
        except Exception as e:
            self.logger.error(f"Failed to get playlist: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_audio_features(self, request: TrackIdsRequest = Body(...)) -> AudioFeaturesResponse:
        try:
            return self._spotify_client_service.get_audio_features(request.track_ids)
        except Exception as e:
            self.logger.error(f"Failed to get audio features: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        