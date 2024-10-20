import os
import logging
from typing import List, Dict
import streamlit as st
import requests
from urllib.parse import urlencode

class HttpClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    

class HttpClientService:            
    logger = logging.getLogger(__name__)
    
    def __init__(self):
        self._url = os.environ.get('BACKEND_URL', 'http://localhost:8000')
    
    def get_chat_response(self, messages: List[Dict[str, str]], api_key: str) -> str:    
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "api_key": api_key,
            "messages": messages
        }
        
        HttpClientService.logger.info(f"Sending chat request to {self._url}/chat")
        
        response = requests.post(f"{self._url}/chat", headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["message"]
        else:
            HttpClientService.logger.error(f"Failed to get chat response: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get chat response")
        
    def get_genius_search(self, query: str) -> Dict:
        encoded_query = urlencode({"query": query})
        url = f"{self._url}/genius/search?{encoded_query}"
        
        HttpClientService.logger.info(f"Sending genius search request to {url}")
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            HttpClientService.logger.error(f"Failed to get genius search: {response.status_code} - {response.text}")
            raise HttpClientError(f"Failed to get genius search")