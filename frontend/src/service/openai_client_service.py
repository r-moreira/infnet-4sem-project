import os
import logging
from openai import OpenAI, OpenAIError, ChatCompletion
from typing import List, Dict
import streamlit as st
import requests

class OpenAIClientSetupError(Exception):
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class OpenAIClientService:            
    def get_backend_chat_response(self, messages: List[Dict[str, str]]) -> str:
        url = os.environ.get('BACKEND_URL', 'http://localhost:8000')
         
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "api_key": st.session_state["api_key"],
            "messages": messages
        }
        
        response = requests.post(f"{url}/chat", headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["message"]
        else:
            logging.error(f"Failed to get chat response: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - {response.text}"