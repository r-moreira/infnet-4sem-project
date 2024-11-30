from typing import Dict
import requests
import logging
from model.genius_model import SongLyricsInfo
from service.genius_scrapper_service import GeniusSongLyricsScrapper

class GeniusClientError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class GeniusClientService:
    def __init__(self, config: Dict) -> None:
        self._config = config
    
    logger = logging.getLogger(__name__)
    
    def search(self, query: str) -> Dict:
        url = f"https://genius.com/api/search?q={query}"
        
        response = requests.get(url)  
            
        if response.status_code == 200:
            return response.json()
        else:
            GeniusClientService.logger.error(f"Failed to get genius search: {response.status_code} - {response.text}")
            raise GeniusClientError(f"Failed to get genius search")
        
    def get_lyrics(self, artist: str, song_name: str) -> SongLyricsInfo:
        LYRICS_NOT_FOUND_RESPONSE = {
                "artist": artist,
                "song_name": song_name,
                "lyrics": "Not found"
            }
        
        artist_id = self._get_artist_id(artist)
        
        if not artist_id:
            return LYRICS_NOT_FOUND_RESPONSE
        
        song_url = self._get_artist_song_lyrics_url(artist_id, song_name)
        
        if not song_url:
            return LYRICS_NOT_FOUND_RESPONSE
        
        lyrics = self._scrap_lyrics(song_url)
        
        if not lyrics:
            return LYRICS_NOT_FOUND_RESPONSE
        
        return {
            "artist": artist,
            "song_name": song_name,
            "lyrics": lyrics
        }
                
    
    def _get_artist_id(self, artist: str) -> int | None:
        url = f"https://genius.com/api/search?q={artist}"
        
        response = requests.get(url)  

        if response.status_code != 200:
            return None
        
        response_hits = response.json()['response']['hits']
        for hit in response_hits:
            if hit['result']['primary_artist']['name'].lower() == artist.lower() or artist.lower() in [name.lower() for name in hit['result']['artist_names']]:
                artist_id = hit['result']['primary_artist']['id']
                return artist_id
        return None
        
    def _get_artist_song_lyrics_url(self, artist_id: int, song_name: str) -> str | None:
        page = 1    
        while True:
            url = f"https://genius.com/api/artists/{artist_id}/songs?page={page}&per_page=50"
            
            print(f"Fetching page {page}...")
            
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch page {page} - {response.text}")
                break
            
            print(f"Page fetched. - {response.json()}")
            
            if response.json()['response']['next_page'] is None:
                break
            
            songs = response.json()['response']['songs']
            
            for song in songs:
                if song['title'].lower() == song_name.lower():
                    return song['url']
        
            page += 1
            
        return None
        
    def _scrap_lyrics(self, song_url: str) -> SongLyricsInfo:
        scrapper = GeniusSongLyricsScrapper(song_url)
        lyrics = scrapper.extract_lyrics()
        
        return lyrics