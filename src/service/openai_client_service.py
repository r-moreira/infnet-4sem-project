import streamlit as st
import openai
import logging
from openai import OpenAI, OpenAIError, ChatCompletion
from typing import List, Dict

class OpenAIClientSetupError(Exception):
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class OpenAIClientService:
    def __init__(self) -> None:
        self._api_key = st.secrets.get("OPEN_AI_API_KEY")
        self._client = None

    def setup_open_ai_client(self) -> OpenAI:
        if not self._api_key:
            if "api_key_set" not in st.session_state:
                st.session_state["api_key_set"] = False

            if not st.session_state["api_key_set"]:
                st.error("Please add your OpenAI API key to the Streamlit secrets.toml file or add below.")
                self._api_key = st.text_input("OpenAI API Key (press enter to confirm)", type="password")
                st.markdown("---")
                st.write("You can create an OpenAI account and get an API key here: https://platform.openai.com/signup")

                if self._api_key:
                    st.session_state["api_key_set"] = True
                    st.session_state["api_key"] = self._api_key
                    st.rerun()
                else:
                    st.stop()
            else:
                self._api_key = st.session_state["api_key"]

        openai.api_key = self._api_key
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