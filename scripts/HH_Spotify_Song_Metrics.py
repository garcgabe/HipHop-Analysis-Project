import pandas as pd
import time, sys, json

from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres

db = Postgres()
spot = SpotifyWrapper()


def get_song_metrics(uris):
    """
    Retrieves audio features for a list of songs.
    
    Args:
        uris (list): A list of song URIs.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the audio features for each song.
    """
    total_songs = len(uris)
    print(f"Fetching audio features for {total_songs} songs.")

    dance, energy, loudness, valence, tempo, instru, speech = ([] for i in range(7))    
    columns = ["dance", "energy", "loudness", "valence", "tempo", "instru", "speech"]

    for count in range(0,5):#total_songs):
    # there's gotta be a better way to do this
        #if(i%50 == 0):
        time.sleep(0.5)
        print("Song # "+str(count)+" of "+ str(total_songs ))
    
    
    
        uri = uris.iloc[count]["song_uri"]
        audio_features = spot.getAudioFeatures(uri)
        print(type(audio_features))
        print(audio_features.keys())
        # if not audio_features:
        #     print("problem detected; manually enter: " + uri)
        #     dance.append(0)
        #     energy.append(0)
        #     loudness.append(0)
        #     valence.append(0)
        #     tempo.append(0)
        #     instru.append(0)
        #     speech.append(0)
        # else:
        # # add song data to lists of metrics
        #     dance.append(audio_features[0]['danceability'])
        #     energy.append(audio_features[0]['energy'])
        #     loudness.append(audio_features[0]['loudness'])
        #     valence.append(audio_features[0]['valence'])
        #     tempo.append(audio_features[0]['tempo'])
        #     instru.append(audio_features[0]['instrumentalness'])
        #     speech.append(audio_features[0]['speechiness'])
    sys.exit(0)
    new_df = pd.concat([pd.Series(dance), pd.Series(energy), pd.Series(loudness),pd.Series(valence),
                                        pd.Series(tempo), pd.Series(instru), pd.Series(speech)],
                                axis=1, keys=columns)
    df = df.reset_index(drop=True)
    return pd.concat([df, new_df], axis=1)
                                        

if __name__=="__main__":
    # Read from album table in DB
    song_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT song_uri FROM songs;
            """), columns = ["song_uri"]
    )

    metrics = get_song_metrics(song_uris)
    print(metrics)
