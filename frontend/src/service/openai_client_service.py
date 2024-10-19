import openai
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
    def __init__(self) -> None:
        self._api_key = None
        self._client = None

    def setup_open_ai_client(self) -> OpenAI:
        openai.api_key = st.session_state["api_key"]
        self._client = openai

    def get_chat_response(self, messages: List[Dict[str, str]]) -> str:
        if self._client is None:
            raise OpenAIClientSetupError(
                "OpenAI client not initialized. Please call setup_open_ai_client() method before calling this method."
            )
        
        try:
            response: ChatCompletion = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            st.error(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")
            
    def get_backend_chat_response(self, messages: List[Dict[str, str]]) -> str:
        url = 'http://localhost:8000/chat'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'ajs_anonymous_id=c55accac-6fd0-48cb-b9a9-7e1479d2ffd8'
        }
        data = {
            "api_key": st.session_state["api_key"],
            "messages": messages
        }
        
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["message"]
        else:
            logging.error(f"Failed to get chat response: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - {response.text}"