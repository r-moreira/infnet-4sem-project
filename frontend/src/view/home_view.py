import streamlit as st
from annotated_text import annotated_text
from view.abstract_strategy_view import AbstractStrategyView
from enums.view_strategy import ViewStrategy

class HomeView(AbstractStrategyView):
       
    def accept(self, view: ViewStrategy) -> bool:
        return view == ViewStrategy.HOME
    
    def show(self) -> None:
        st.title("Welcome to the Deep Listen App! 🎧")
        
        st.markdown("""
            The Deep Listen App is designed to provide in-depth analysis of the audio features of songs, albums, and playlists. By leveraging the power of Spotify's API, lyrical content, and advanced language models (LLMs), this project aims to offer a comprehensive understanding of musical compositions and their characteristics.
        """)
        
        st.divider()
        
        st.subheader("Audio Features Explained 📊")
        
        features = [
            ("Danceability", "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.", "0.0", "least danceable", "1.0", "most danceable"),
            ("Energy", "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.", "0.0", "low energy", "1.0", "high energy"),
            ("Key", "The key the track is in. Integers map to pitches using standard Pitch Class notation (e.g., 0 = C, 1 = C♯/D♭, 2 = D, and so on).", "0", "C", "11", "B"),
            ("Loudness", "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing the relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude).", "-60 dB", "very quiet", "0 dB", "very loud"),
            ("Mode", "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.", "0", "minor", "1", "major"),
            ("Speechiness", "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g., talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.", "0.0", "music", "1.0", "speech"),
            ("Acousticness", "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.", "0.0", "not acoustic", "1.0", "acoustic"),
            ("Instrumentalness", "Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.", "0.0", "vocal", "1.0", "instrumental"),
            ("Liveness", "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.", "0.0", "studio", "1.0", "live"),
            ("Valence", "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g., happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g., sad, depressed, angry).", "0.0", "negative", "1.0", "positive"),
            ("Tempo", "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.", "40 BPM", "slow", "200 BPM", "fast"),
            ("Duration (ms)", "The duration of the track in milliseconds.", "0 ms", "short", "300000 ms", "long"),
            ("Time Signature", "An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).", "3", "waltz", "4", "common time")
        ]
        
        for feature in features:
            st.markdown(f"**{feature[0]}**: {feature[1]}")
            annotated_text(
                f"",
                (feature[2], feature[3], "#222"),
                " to ",
                (feature[4], feature[5], "#222")
            )
            st.markdown("---")