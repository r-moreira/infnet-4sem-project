import openai
from openai import OpenAI, OpenAIError, ChatCompletion
from typing import List, Dict

class OpenAIClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class OpenAIClientService:
    def get_chat_response(self, messages: List[Dict[str, str]], api_key: str) -> str:
        if not api_key:
            raise OpenAIClientError("API Key is required.")
        
        openai.api_key = api_key
        client: OpenAI = openai
        
        try:
            response: ChatCompletion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            raise OpenAIClientError(f"An error occurred: {e}")