import streamlit as st
from view.abstract_view import AbstractView
from enums.view_strategy import ViewStrategy
from streamlit_option_menu import option_menu 
from streamlit_extras.add_vertical_space import add_vertical_space
from service.session_state_service import SessionStateService

class SidebarView(AbstractView):
    def __init__(self, session_state_service: SessionStateService) -> None:
        self._session_state_service = session_state_service
    
    def show(self) -> ViewStrategy:
        with st.sidebar:
            add_vertical_space(2)
            
            st.title("🤖 Deep Listen 🎸")
            
            add_vertical_space(4)
             
            strategy: ViewStrategy = self._option_menu()
            
            st.divider()
            st.markdown("🎵 **Deep Listen** is a powerful music analysis tool that leverages the Spotify API and advanced language models (LLMs)")
            st.markdown("Discover detailed insights into the audio features of your favorite tracks and playlists, and gain a deeper understanding of the music you love.")
          
            return strategy
       
    def _option_menu(self) -> ViewStrategy:
        menu_index = None
        
        if self._session_state_service.is_view_menu_option():
            menu_index = ViewStrategy.to_value_list().index(self._session_state_service.get_view_menu_option())

        strategy = option_menu(
            "Main Menu", 
            ViewStrategy.to_value_list(), 
            icons=[
                'house-fill',
                'music-note-beamed'
            ],
            menu_icon="cast", 
            default_index=menu_index if menu_index is not None else 0,
            key=f"sidebar_view_menu"
        )
        
        self._session_state_service.set_view_menu_option(strategy)
        return ViewStrategy(strategy)