import logging
import streamlit as st
from enums.view_strategy import ViewStrategy

class SessionStateService:
    logger = logging.getLogger(__name__)
    
    def set_view_menu_option(self, menu_option: str) -> None:
        SessionStateService.logger.info(f"menu_option: {menu_option}")
        
        if menu_option not in ViewStrategy.to_value_list():
            raise ValueError(f"Invalid menu option: {menu_option}")

        st.session_state["sidebar_menu_option"] = menu_option
        
    def get_view_menu_option(self) -> str:
        if "sidebar_menu_option" not in st.session_state:
            SessionStateService.set_view_menu_option(ViewStrategy.ALBUM_ANALYSIS.value)
        
        return st.session_state["sidebar_menu_option"]

    def is_view_menu_option(self) -> bool:
        return "sidebar_menu_option" in st.session_state
    
    def initialize_chat_session(self) -> None:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
            
    def append_user_chat_message(self, message: str) -> None:
        st.session_state.messages.append({"role": "user", "content": message})
        
    def append_assistant_chat_message(self, message: str) -> None:
        st.session_state.messages.append({"role": "assistant", "content": message})
    
    def initialize_openai_api_key_handler(self) -> None:
        if "api_key_set" not in st.session_state:
            st.session_state["api_key_set"] = False
            st.session_state["api_key"] = None
    
    def set_openai_api_key(self, api_key: str) -> None:
        st.session_state["api_key"] = api_key
        st.session_state["api_key_set"] = True
        
    def get_openai_api_key(self) -> str:
        return st.session_state["api_key"]