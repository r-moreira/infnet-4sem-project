from view.abstract_strategy_view import AbstractStrategyView
from enums.view_strategy import ViewStrategy
from service.session_state_service import SessionStateService
from service.http_client_service import HttpClientService
import logging 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu 
from typing import List, Tuple, Dict

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
        
        st.header("Playlist Analysis 📊")
        
        add_vertical_space(1)
        
        st.subheader("Instructions:")
        
        st.markdown("""
            1. Enter a Spotify Playlist URL, like: https://open.spotify.com/playlist/2VTOQEarWbJOhKwGhQjMBH
            2. Press Enter
            3. Wait for the dashboard and AI to generate an explanation of the audio features of the playlist
        """)
        
        st.divider()
        
        url = st.text_input("Enter the playlist URL")
        
        if url:
            playlist = self.get_cached_playlist(url.strip())
            
            iframe_html = f"""
                <div style="display: flex; justify-content: center;">
                    <iframe src="https://open.spotify.com/embed/playlist/{playlist['id']}" width="2000" height="600" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                </div>
            """
            
            with st.container():
                st.components.v1.html(iframe_html, height=600)
            
            add_vertical_space(2)
            strategy = self.playlist_menu()
        
            if strategy == "Audio Features":
            
                track_ids = [item['track']['id'] for item in playlist['tracks']['items']]
                audio_features = self.get_cached_audio_features(track_ids)     
                metrics = audio_features['metrics']
                
                self.show_audio_feature_statistics(metrics)
                            
                with st.spinner("Generating Explanation..."):
                    with st.expander("Audio Features AI Generated Explanation"):
                        explanation = self.get_cached_audio_features_explanation(playlist, metrics)
                        st.header("Audio Features AI Generated Explanation:")
                        st.markdown(explanation)
                        st.download_button(
                            label="Download Audio Features Json",
                            data=str(audio_features),
                            file_name="audio_features.json",
                            mime="application/json"
                        )
            else:                
                lyrics_found_list, lyrics_not_found_list = self.get_cached_playlist_lyrics(playlist)                
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("IA Generated All Lyrics Resume")
                    
                    resume = self.get_cached_playlist_lyrics_resume(lyrics_found_list)
                    st.markdown(resume)
                
                with col2:
                    st.header("Lyrics Viewer")
                    current_lyrics = st.selectbox(
                        "Select a lyrics",
                        format_func=lambda x: f"{x['artist']} - {x['song_name']}", 
                        options=lyrics_found_list
                    )
                    st.markdown(current_lyrics["lyrics"].replace('\n', '<br>'), unsafe_allow_html=True)
                    
                    col2_1, col2_2 = st.columns([3, 1], vertical_alignment="center")
                    with col2_1:
                        with st.expander(f"View missing lyrics ({len(lyrics_not_found_list)})"):
                            for lyrics in lyrics_not_found_list:
                                st.write(f"{lyrics['artist']} - {lyrics['song_name']}")
                    with col2_2:        
                        st.download_button(
                            label="Download all lyrics",
                            data=str(lyrics_found_list),
                            file_name="lyrics.json",
                            mime="application/json", 
                            use_container_width=True
                        )

    @st.cache_data(ttl=3600, show_spinner=True) 
    def get_cached_playlist_lyrics_resume(_self, lyrics_found_list):
        return _self._http_client_service.get_playlist_lyrics_resume(lyrics_found_list)

    @st.cache_data(ttl=3600, show_spinner=True) 
    def get_cached_playlist_lyrics(_self, playlist) -> Tuple[List[Dict], List[Dict]]:
        lyrics_found_list = []
        lyrics_not_found_list = []
        for item in playlist['tracks']['items']:
            track = item['track']
            song_name = track['name']
            artist = track['artists'][0]['name']
           
            lyrics_info = _self.get_cached_song_lyrics(song_name, artist)
                    
            if lyrics_info["lyrics"] != "Lyrics not found":
                lyrics_found_list.append(lyrics_info)
            else:
                lyrics_not_found_list.append(lyrics_info)
        return lyrics_found_list, lyrics_not_found_list
                
    @st.cache_data(ttl=3600, show_spinner=False)
    def get_cached_song_lyrics(_self, song_name, artist):
        return _self._http_client_service.get_song_lyrics(song_name, artist)

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_cached_audio_features_explanation(_self, playlist, metrics):
        return _self._http_client_service.get_playlist_audio_features_explanation(
                    playlist['name'],
                    playlist['description'],
                    metrics
                )

    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_playlist(_self, url):
        return _self._http_client_service.get_playlist(url)
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def get_cached_audio_features(_self, track_ids):
        return _self._http_client_service.get_audio_features(track_ids)
    
    def playlist_menu(self):
        return option_menu(
                "Option Menu", 
                options=["Audio Features", "Lyrics"], 
                icons=[
                    'music-note-list',
                    'file-text',
                ],
                orientation="horizontal",
                menu_icon="cast", 
                default_index=0,
                key=f"playlist_view_menu"
            )
    
    def show_audio_feature_statistics(self, metrics):
        mean_metrics = {
                "Danceability": float(metrics["mean_danceability"]),
                "Energy": float(metrics["mean_energy"]),
                "Speechiness": float(metrics["mean_speechiness"]),
                "Acousticness": float(metrics["mean_acousticness"]),
                "Instrumentalness": float(metrics["mean_instrumentalness"]),
                "Liveness": float(metrics["mean_liveness"]),
                "Valence": float(metrics["mean_valence"]),
            }
        
        col1, col2, col3 = st.columns(3)
            
        with col1:
            fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = float(metrics["mean_tempo"]),
                    title = {'text': "Mean Tempo (BPM)"},
                    gauge={
                            'bar': {'color': "#636EFA"},
                            'axis': {'range': [0, 200]}
                        }
                    ))
            
            st.plotly_chart(fig, use_container_width=True)   
            
        with col2:    
            fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = float(metrics["mean_duration_ms"]) / 1000,
                    title = {'text': "Mean Duration (Seconds)"},
                    gauge={
                            'bar': {'color': "#EF553B"},
                            'axis': {'range': [0, 600]}
                        }
                    ))
            st.plotly_chart(fig, use_container_width=True) 
                
        with col3:
            fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = float(metrics["mean_loudness"]),
                    title = {'text': "Mean Loudness (DB)"},
                    gauge={
                            'bar': {'color': "#00CC96"},
                            'axis': {'range': [-60, 0]}
                        }
                    ))
            st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(
                x=list(mean_metrics.keys()), 
                y=list(mean_metrics.values()), 
                labels={'x': 'Audio Features', 'y': 'Value'},
                title="Mean Audio Features",
                color=list(mean_metrics.keys()),
                color_discrete_sequence=px.colors.qualitative.Plotly,
            )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
        
        mode_count = metrics["mode_count"]
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                    x=list(mode_count.keys()), 
                    y=list(mode_count.values()), 
                    labels={'x': 'Mode', 'y': 'Count'},
                    title="Mode Count",
                    color=mode_count.keys(),
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                )
            st.plotly_chart(fig)
            
        with col2:
            fig = px.pie(
                    names=list(mode_count.keys()), 
                    values=list(mode_count.values()), 
                    title="Mode Distribution",
                    color=mode_count.keys(),
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                )
            st.plotly_chart(fig)
        
        key_count = metrics["key_count"]
        fig = px.bar(
                x=list(key_count.keys()), 
                y=list(key_count.values()), 
                labels={'x': 'Key', 'y': 'Count'},
                title="Key Count",
                color=key_count.keys(),
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
        st.plotly_chart(fig)