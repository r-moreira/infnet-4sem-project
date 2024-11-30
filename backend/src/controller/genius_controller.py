from fastapi import APIRouter, HTTPException, Query
from service.genius_client_service import GeniusClientService
from model.genius_model import SongLyricsInfo
import logging

class GeniusController:
    logger = logging.getLogger(__name__)
    
    def __init__(self, genius_client_service: GeniusClientService) -> None:
        self._genius_client_service = genius_client_service
        self.router = APIRouter(prefix="/genius")
        self.router.add_api_route("/search", self.search, methods=["GET"])
        self.router.add_api_route("/lyrics", self.get_lyrics, methods=["GET"])
        
    async def search(self, query: str = Query(..., description="Search query")):
        try:
            self.logger.info(f"Searching for {query}")
            return self._genius_client_service.search(query)
        except Exception as e:
            self.logger.error(f"Failed to get genius search: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_lyrics(
            self, 
            artist: str = Query(..., description="Artist name"), 
            song_name: str = Query(..., description="Song name")
        ) -> SongLyricsInfo:
        try:
            self.logger.info(f"Getting lyrics for {artist} - {song_name}")  
            return self._genius_client_service.get_lyrics(artist, song_name)
        except Exception as e:
            self.logger.error(f"Failed to get lyrics: {e}")
            raise HTTPException(status_code=500, detail=str(e))