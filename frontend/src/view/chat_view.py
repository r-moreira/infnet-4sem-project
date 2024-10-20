import streamlit as st
from service.http_client_service import HttpClientService
from service.session_state_service import SessionStateService
from view.abstract_strategy_view import AbstractStrategyView
from enums.view_strategy import ViewStrategy
import logging

class ChatView(AbstractStrategyView):
    logger = logging.getLogger(__name__)
    
    def __init__(self, 
                 session_state_service: SessionStateService,
                 http_client_service: HttpClientService) -> None:
        self._http_client_service = http_client_service
        self._api_key = st.secrets.get("OPEN_AI_API_KEY")
        self._session_state_service = session_state_service
        self._session_state_service.initialize_chat_session()

    def accept(self, view: ViewStrategy) -> bool:
        return view == ViewStrategy.CHAT

    def show(self) -> None:
        self._handle_api_key()
        
        st.title("💬 Chatbot")
        for message in st.session_state.messages:
            st.chat_message(message["role"]).write(message["content"])

        if prompt := st.chat_input():
            self._on_chat_submit(prompt)

    @st.cache_data(show_spinner=False)
    def _on_chat_submit(_self, prompt: str) -> None:
        _self._session_state_service.append_user_chat_message(prompt)
        
        st.chat_message("user").write(prompt)
        
        message: str = _self._http_client_service.get_chat_response(st.session_state.messages)
        
        _self._session_state_service.append_assistant_chat_message(message)
        
        st.chat_message("assistant").write(message)

    def _handle_api_key(self) -> None:
        if not self._api_key:
            if "api_key_set" not in st.session_state:
                st.session_state["api_key_set"] = False

            if not st.session_state["api_key_set"]:
                st.warning("Please add your OpenAI API key to the Streamlit secrets.toml file or add below.")
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
        else:
            st.session_state["api_key_set"] = True
            st.session_state["api_key"] = self._api_key