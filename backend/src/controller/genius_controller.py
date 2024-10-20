from fastapi import APIRouter, HTTPException, Query
from service.genius_client_service import GeniusClientService

class GeniusController:
    
    def __init__(self, genius_client_service: GeniusClientService) -> None:
        self._genius_client_service = genius_client_service
        self.router = APIRouter(prefix="/genius")
        self.router.add_api_route("/search", self.search, methods=["GET"])
        
    def search(self, query: str = Query(..., description="Search query")):
        try:
            response = self._genius_client_service.search(query)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))