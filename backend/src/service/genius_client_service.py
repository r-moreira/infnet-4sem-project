from typing import Dict
import requests
import logging

class GeniusClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class GeniusClientService:
    logger = logging.getLogger(__name__)
    
    def search(self, query: str) -> Dict:
        url = f"https://genius.com/api/search?q={query}"
        
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            GeniusClientService.logger.error(f"Failed to get genius search: {response.status_code} - {response.text}")
            raise GeniusClientError(f"Failed to get genius search")