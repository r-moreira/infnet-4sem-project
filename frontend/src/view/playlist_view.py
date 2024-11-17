from view.abstract_strategy_view import AbstractStrategyView
from enums.view_strategy import ViewStrategy
from service.session_state_service import SessionStateService
from service.http_client_service import HttpClientService
import logging 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space

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
            1. Enter a Spotify Playlist URL, like: https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF
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
            
            track_ids = [item['track']['id'] for item in playlist['tracks']['items']]
            audio_features = self._http_client_service.get_audio_features(track_ids)                    
            metrics = audio_features['metrics']
            
            self.show_audio_feature_statistics(metrics)
                        
            with st.spinner("Generating Explanation..."):
                explanation = self.get_cached_audio_features_explanation(playlist, metrics)
                st.header("AI Generated Explanation:")
                st.markdown(explanation)
            
            with st.expander("Audio Features Json"):
                st.write(audio_features)
                st.download_button(
                    label="Download",
                    data=str(audio_features),
                    file_name="audio_features.json",
                    mime="application/json"
                )

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
                    title = {'text': "Mean Tempo (BPM)"}))
            st.plotly_chart(fig, use_container_width=True)   
            
        with col2:    
            fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = float(metrics["mean_duration_ms"]) / 1000,
                    title = {'text': "Mean Duration (Seconds)"}))
            st.plotly_chart(fig, use_container_width=True) 
                
        with col3:
            fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = float(metrics["mean_loudness"]),
                    title = {'text': "Mean Loudness (dB)"}))
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