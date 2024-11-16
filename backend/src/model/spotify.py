from pydantic import BaseModel
from typing import List, Dict, Optional

def float_encoder(value: float) -> str:
    return format(value, '.6f')

class Image(BaseModel):
    url: str

class Owner(BaseModel):
    display_name: str

class ExternalUrls(BaseModel):
    spotify: str

class Artist(BaseModel):
    name: str

class Album(BaseModel):
    name: str

class Track(BaseModel):
    album: Album
    artists: List[Artist]
    name: str
    id: str

class TrackItem(BaseModel):
    track: Track

class Tracks(BaseModel):
    items: List[TrackItem]
    total: int

class Playlist(BaseModel):
    images: List[Image]
    owner: Owner
    external_urls: ExternalUrls
    tracks: Tracks
    name: str
    description: str
    id: str
    
class AudioFeatures(BaseModel):
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    type: str
    id: str
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int
    
class AudioFeaturesModesCount(BaseModel):
    major: int
    minor: int    
    
class AudioFeaturesKeysCount(BaseModel):
    C: int
    C_sharp: int
    D: int
    D_sharp: int
    E: int
    F: int
    F_sharp: int
    G: int
    G_sharp: int
    A: int
    A_sharp: int
    B: int

class AudioFeaturesMetrics(BaseModel):
    mean_danceability: float
    mean_energy: float
    mean_loudness: float
    mean_speechiness: float
    mean_acousticness: float
    mean_instrumentalness: float
    mean_liveness: float
    mean_valence: float
    mean_tempo: float
    mode_count: AudioFeaturesModesCount
    key_count: AudioFeaturesKeysCount
    
    class Config:
        json_encoders = {
            float: float_encoder
        }

class AudioFeaturesResponse(BaseModel):
    audio_features: List[AudioFeatures]
    metrics: AudioFeaturesMetrics

class TrackIdsRequest(BaseModel):
    track_ids: List[str]
    