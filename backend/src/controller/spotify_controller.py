from fastapi import APIRouter, HTTPException, Query
from service.spotify_client_service import SpotifyClientService
from typing import Dict, List
from model.spotify import Playlist

class SpotifyController:
    
    def __init__(self, spotify_client_service: SpotifyClientService) -> None:
        self.spotify_client_service = spotify_client_service
        self.router = APIRouter(prefix="/spotify")
        self.router.add_api_route("/playlist", self.get_playlist, methods=["GET"])
  
    async def get_playlist(self, url: str = Query(...)) -> Playlist:
        try:
            playlist = self.spotify_client_service.get_playlist(url)
            return playlist
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        