import streamlit as st
from view.abstract_view import AbstractView
from enums.view_strategy import ViewStrategy
from typing import Literal

class SidebarView(AbstractView):
    
    @staticmethod
    def show() -> ViewStrategy:
        st.sidebar.title("🤖 Deep Listen 🎸")
        st.sidebar.markdown("---")
        st.sidebar.markdown("This app is a chatbot that uses OpenAI's GPT-4 model to generate responses to analyze and discuss music.")
        st.sidebar.markdown("The chat is in beta, it works, but like a normal Chat GPT chat, music features will be added soon.")
        st.sidebar.markdown("---")
        
        strategy: str = st.sidebar.radio("Select APP Mode:", options=ViewStrategy.to_value_list(), index=0)
        
        return ViewStrategy(strategy)
       