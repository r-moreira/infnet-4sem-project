from view.abstract_view import AbstractView
from utils.streamlit_utils import StreamlitUtils
from view.api_key_view import ApiKeyView
from view.chat_view import ChatCallbackProvider
import os
import requests
import streamlit as st

class MainView(AbstractView):
    def __init__(
        self, 
        sidebar_view: AbstractView,
        album_analysis_view: AbstractView,
        api_key_view: AbstractView,
        chat_view: AbstractView,
        chat_view_callbacks: ChatCallbackProvider,
        ) -> None:
        
        self._sidebar_view = sidebar_view
        self._album_analysis_view = album_analysis_view
        self._chat_view = chat_view
        self._chat_view_callbacks = chat_view_callbacks
        self._api_key_view = api_key_view
        
    def show(self) -> None:
        StreamlitUtils.setup_page_config()
        
        app_mode = self._sidebar_view.show()

        backend_url = os.getenv('BACKEND_URL', 'http://localhost:8000')

        response = requests.get(f"{backend_url}/hello")
        data = response.json()


        st.write(f"Backend data: {data}")
        
        if app_mode == "Album Analisys":
            self._album_analysis_view.show()
        else:
            self._api_key_view.show()
            self._chat_view.show(self._chat_view_callbacks.on_chat_submit)