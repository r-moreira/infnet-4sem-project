import streamlit as st
import pandas as pd
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from view.abstract_view import AbstractView

DEFAULT_ALBUM = "data/processed/albums_collection_lyrics.csv"

CSV_FILE_SCHEMA = """
   * album_name: ```str```
   * artist_name: ```str```
   * song_name: ```str```
   * lyrics: ```str```
"""

EXPECTED_COLUMNS = ["album_name", "artist_name", "song_name", "lyrics"]

class AlbumAnalysisView(AbstractView):
    def __init__(self) -> None:
        self._album_data = pd.DataFrame()
                
    def show(self) -> None:
        self._display_header()
        self._fetch_album()
        self._upload_album()
        self._display_album_info()
        self._download_album()
        self._display_album_word_cloud()
                
    @staticmethod
    def _display_header() -> None:
        st.title("🎵 Album Analysis")
        st.markdown("This is the music info page, you can upload, download and analyze albums data.")
                    
    @staticmethod
    def _get_table_download_link(df: pd.DataFrame) -> str:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
        return href
    
    def _fetch_album(self, pattern: str = "*_lyrics.csv") -> None:
        self._album_data = pd.read_csv(DEFAULT_ALBUM)
        
    def _upload_album(self) -> None:       
        st.markdown("---")
        st.markdown("#### Upload a CSV file with the following schema:")
        st.markdown(CSV_FILE_SCHEMA)
        uploaded_file = st.file_uploader("Upload a file to analyze", type=["csv"], label_visibility="hidden")
        
        if uploaded_file is not None:
            try:
                tmp_album_data = pd.read_csv(uploaded_file)
                
                if tmp_album_data.columns.equals(self._album_data.columns):
                    self._album_data = tmp_album_data
                    st.success("File uploaded successfully!")
                else:
                    st.error(f"Invalid file columns. Expected: {EXPECTED_COLUMNS}")
                
            except pd.errors.EmptyDataError as e:
                st.error(f"The file data must no be empty: {e}")
                return
            except pd.errors.ParserError as e:
                st.error(f"Invalid file: {e}")
                return
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return
       
    def _download_album(self) -> None:
        if not self._album_data.empty:
            csv = self._album_data.to_csv(index=False)
            st.download_button(
                label="Download Albuns Data",
                data=csv,
                file_name='albums_data.csv',
                mime='text/csv',
            )

    def _display_album_info(self) -> None:
        if self._album_data.empty:
            return
        
        st.markdown("---")
        album_names = self._album_data['album_name'].unique()
        artist_names = self._album_data['artist_name'].unique()
        song_names = self._album_data['song_name'].unique()

        filter_type = st.selectbox("Select Filter Type", ["Album", "Artist", "Music"])

        if filter_type == "Album":
            selected_album = st.multiselect("Select Album(s)", album_names)
            if selected_album:
                self._album_data = self._album_data[self._album_data['album_name'].isin(selected_album)]
        elif filter_type == "Artist":
            selected_artist = st.multiselect("Select Artist(s)", artist_names)
            if selected_artist:
                self._album_data = self._album_data[self._album_data['artist_name'].isin(selected_artist)]
        elif filter_type == "Music":
            selected_song = st.multiselect("Select Music(s)", song_names)
            if selected_song:
                self._album_data = self._album_data[self._album_data['song_name'].isin(selected_song)]

        if self._album_data.empty:
            st.warning("No data available for the selected filters.")
        else:
            if self._album_data['album_name'].nunique() == 1:
                st.markdown(f"#### Album: {self._album_data.iloc[0]['album_name']} by {self._album_data.iloc[0]['artist_name']}")
                st.write(self._album_data[['song_name', 'lyrics']])
            elif self._album_data['artist_name'].nunique() == 1: 
                st.markdown(f"#### {self._album_data['album_name'].nunique()} Albums by {self._album_data.iloc[0]['artist_name']}")
                st.write(self._album_data[['album_name', 'song_name', 'lyrics']])
            else: 
                st.markdown(f"#### {self._album_data['album_name'].nunique()} Albums by {self._album_data['artist_name'].nunique()} Artists")
                st.write(self._album_data[['album_name', 'artist_name', 'song_name', 'lyrics']])
                    

    
    def _display_album_word_cloud(self) -> None:
        if self._album_data.empty:
            return
        
        st.markdown("---")
        st.markdown("#### Lyrics Word Cloud")
        
        text = ' '.join(self._album_data['lyrics'].astype(str))
        text = self._clean_text(text)
        
        wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Blues').generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
        
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\[.*?\]', '', text)
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(words)