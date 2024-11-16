from view.abstract_strategy_view import AbstractStrategyView
from enums.view_strategy import ViewStrategy
from service.session_state_service import SessionStateService
from service.http_client_service import HttpClientService
import logging 
import streamlit as st

class PlaylistView(AbstractStrategyView):
    logger = logging.getLogger(__name__)
    
    def __init__(
            self, 
            session_state_service: SessionStateService,
            http_client_service: HttpClientService
        ) -> None:
        
        self._http_client_service = http_client_service
        self._session_state_service = session_state_service
        
    def accept(self, view: ViewStrategy) -> bool:
        return view == ViewStrategy.PLAYLIST
    
    def show(self) -> None:
        self.logger.info("Showing Playlist View")
        
        url = st.text_input("Enter the playlist URL")
        
        if url:
            playlist = self._http_client_service.get_playlist(url)
            
            iframe_html = f"""
                <div style="display: flex; justify-content: center;">
                    <iframe src="https://open.spotify.com/embed/playlist/{playlist['id']}" width="600" height="600" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                </div>
            """
            
            with st.container():
                st.components.v1.html(iframe_html, height=600)
            
            #st.write(playlist)
            
            track_ids = [item['track']['id'] for item in playlist['tracks']['items']]
            audio_features = self._http_client_service.get_audio_features(track_ids)            
            
            st.write(audio_features)