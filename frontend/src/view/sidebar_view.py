import streamlit as st
from view.abstract_view import AbstractView
from enums.view_strategy import ViewStrategy
from streamlit_option_menu import option_menu 
from streamlit_extras.add_vertical_space import add_vertical_space

class SidebarView(AbstractView):
    
    @staticmethod
    def show() -> ViewStrategy:
        with st.sidebar:
            add_vertical_space(2)
            
            st.title("🤖 Deep Listen 🎸")
            
            add_vertical_space(4)
            
            strategy = option_menu(
                "Main Menu", 
                ViewStrategy.to_value_list(), 
                icons=[
                    'music-note-list',
                    'music-note-beamed',
                    'chat'
                ],
                menu_icon="cast", 
                default_index=0
            )
            
            st.divider()
            
            st.markdown("This app is a chatbot that uses OpenAI's GPT-4 model to generate responses to analyze and discuss music.")
            st.markdown("The chat is in beta, it works, but like a normal Chat GPT chat, music features will be added soon.")
           
        return ViewStrategy(strategy)
       