import openai
import logging
from openai import OpenAI, OpenAIError, ChatCompletion
from typing import List, Dict
import streamlit as st

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