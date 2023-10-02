from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

class SpotifyWrapper():
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, 
                                                              client_secret=SPOTIFY_CLIENT_SECRET)
        self.spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager,
                                    retries=10, status_retries=10)

    def getAlbumsTracks(self, album_id):
        return self.spot.album_tracks(album_id)
    
    def getAudioFeatures(self, song_uri):
        return self.spot.audio_features(song_uri)
    
    def searchArtist(self, artist):
        return self.spot.search(q=artist, type="artist")
    
    def getAlbums(self, artist_uri):
        return self.spot.artist_albums(artist_uri, album_type="album")