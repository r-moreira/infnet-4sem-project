from typing import Dict
import requests

class GeniusClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class GeniusClientService:
    
    def search(self, query: str) -> Dict:
        url = f"https://genius.com/api/search?q={query}"
        
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            raise GeniusClientError(f"An error occurred: {response.status_code} - {response.text}")