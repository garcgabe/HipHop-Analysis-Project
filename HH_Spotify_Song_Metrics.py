import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time, sys

class spotWrapper():
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

def get_song_metrics(df):
    spot = spotWrapper()
    dance, energy, loudness, valence, tempo, instru, speech = ([] for i in range(7))
    all_uris = df["song_uri"]
    print(df)
    columns = ["dance", "energy", "loudness", "valence", "tempo", "instru", "speech"]
    print(columns)
    length = 2#len(all_uris)
    for i in range(0,length):
        print(i)
        if(i%50 == 0):
            time.sleep(0.5)
            print("Song # "+str(i)+" of "+ str(length ))
        uri = all_uris[i]
        print(uri)
        spot_audio = spot.getAudioFeatures(uri)
        if(spot_audio == None):
            print("problem detected: " + uri)
            dance.append(0)
            energy.append(0)
            loudness.append(0)
            valence.append(0)
            tempo.append(0)
            instru.append(0)
            speech.append(0)
        else:
        # add song data to lists of metrics
            dance.append(spot_audio[0]['danceability'])
            energy.append(spot_audio[0]['energy'])
            loudness.append(spot_audio[0]['loudness'])
            valence.append(spot_audio[0]['valence'])
            tempo.append(spot_audio[0]['tempo'])
            instru.append(spot_audio[0]['instrumentalness'])
            speech.append(spot_audio[0]['speechiness'])
    new_df = pd.concat([pd.Series(dance), pd.Series(energy), pd.Series(loudness),pd.Series(valence),
                                        pd.Series(tempo), pd.Series(instru), pd.Series(speech)],
                                axis=1, keys=columns)
    df = df.reset_index(drop=True)
    #new_df = new_df.reset_index(drop=True)
    return pd.concat([df, new_df], axis=1)
                                        

if __name__=="__main__":
    main = pd.read_excel("SpotifySongs.xlsx")
    with_metrics = get_song_metrics(main)
    print(with_metrics)
    with_metrics.to_excel("SpotifySongsMetrics.xlsx")