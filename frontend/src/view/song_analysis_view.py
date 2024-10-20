from enums.view_strategy import ViewStrategy
from view.abstract_strategy_view import AbstractStrategyView
import streamlit as st

class SongAnalysisView(AbstractStrategyView):
    def __init__(self, http_client_service) -> None:
        self._http_client_service = http_client_service
    
    
    def accept(self, view: ViewStrategy) -> bool:
        return view == ViewStrategy.SONG_ANALYSIS
                
    def show(self) -> None:
        st.title("🎵 Song Analysis")
        
        st.write("More features coming soon!")
        
        st.divider()
        
        song_name = st.text_input("Search for a song", key="song_search")
        
        if song_name:
            response = self._http_client_service.get_genius_search(song_name)
            
            st.json(response)