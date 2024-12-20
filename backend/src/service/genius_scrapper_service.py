import requests
from bs4 import BeautifulSoup

class GeniusSongLyricsScrapper:
    def __init__(self, song_url: str):
        self.song_url = song_url
        self._soup = None

    @property
    def soup(self) -> BeautifulSoup:
        if not self._soup:
            self.fetch_page()
        return self._soup

    def fetch_page(self) -> None:
        response = requests.get(self.song_url)
        response.raise_for_status() 
        self._soup = BeautifulSoup(response.text, 'html.parser')

    def extract_lyrics(self) -> str | None:
        instrumental_message = self.soup.select_one('div.LyricsPlaceholder-sc-99de6a4b-2')
        if instrumental_message and 'This song is an instrumental' in instrumental_message.text:
            return 'This song is an instrumental'
        
        lyrics_div = self.soup.select_one('div[data-lyrics-container="true"]')
        if not lyrics_div:
            return None
        
        lyrics = []
        for element in lyrics_div.descendants:
            if element.name == 'br':
                lyrics.append('\n')
            elif isinstance(element, str):
                lyrics.append(element)
        
        return ''.join(lyrics)

    def extract_song_name(self) -> str | None:
        song_name_span = self.soup.select_one('h1 span[class*="SongHeader-desktop-sc-b6d678d2-11 dWLjHo"]')
        if not song_name_span:
            return None
        
        return song_name_span.text
    
    def extract_album_name(self) -> str | None:
        album_name_div = self.soup.select_one('div.HeaderArtistAndTracklist-desktop-sc-dc27fea8-2 a')
        if not album_name_div:
            return None
        
        return album_name_div.text.strip()
    
    def extract_artist_name(self) -> str | None:
        artist_name_div = self.soup.select_one('div.HeaderArtistAndTracklist-desktop-sc-dc27fea8-1 span.PortalTooltip-sc-e6affa6e-1 a')
        if not artist_name_div:
            return None
        
        return artist_name_div.text.strip()