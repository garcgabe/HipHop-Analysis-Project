
class Spotify:
    def __init__(self):
        # Hide these within venv variables
        client_id = 'accd0aa479164ddcbf1cbf822512b80b'
        client_secret = '58bfc467435045e7b61c86fb03385729'
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager,
                                    retries=10, status_retries=10)

    def getAlbumsTracks(self, id):
        return self.spot.album_tracks(id)
    def getAudioFeatures(self, song_uri):
        return self.spot.audio_features(song_uri)