import requests
from bs4 import BeautifulSoup

class GeniusAlbumSongsCrawler:
    def __init__(self, album_url: str):
        self.album_url = album_url
        self._soup = None

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    def fetch_page(self) -> BeautifulSoup:
        response = requests.get(self.album_url)
        response.raise_for_status()  
        self._soup = BeautifulSoup(response.text, 'html.parser')
        return self._soup

    def extract_song_links(self) -> list:
        if not self._soup:
            raise ValueError("Soup not initialized. Call fetch_page() first.")
        
        song_links = []
        for link in self._soup.select('a.u-display_block'):
            href = link.get('href')
            if href:
                song_links.append(href)
        return song_links
