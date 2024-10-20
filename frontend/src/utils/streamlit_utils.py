import streamlit as st

class StreamlitUtils:
    
    @staticmethod
    def setup_page_config() -> None:
        st.set_page_config(
            page_title="Deep Listen - An Intelligent Music Assistant",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="auto"
        )