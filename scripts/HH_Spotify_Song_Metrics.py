import pandas as pd
import time, sys, json

from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres

db = Postgres()
spot = SpotifyWrapper()


def get_song_metrics(uris):
    spot = spotWrapper()
 
    dance, energy, loudness, valence, tempo, instru, speech = ([] for i in range(7))
    
    all_uris = df["song_uri"]
    #print(df)
    columns = ["dance", "energy", "loudness", "valence", "tempo", "instru", "speech"]
    #print(columns)
    length = len(all_uris)
    for i in range(0,length):
        print(i)
        if(i%50 == 0):
            time.sleep(0.5)
            print("Song # "+str(i)+" of "+ str(length ))
        uri = all_uris[i]
        print(uri)
        spot_audio = spot.getAudioFeatures(uri)
        if(spot_audio == None):
            print("problem detected; manually enter: " + uri)
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
    return pd.concat([df, new_df], axis=1)
                                        

if __name__=="__main__":
    main = pd.read_csv("S3 Data/SpotifySongs")
    with_metrics = get_song_metrics(main)
    with_metrics = with_metrics.drop( [_ for _ in with_metrics.columns if "Unnamed" in _]  , axis=1)
    with_metrics.index.name = "index"
    print(with_metrics)
    with_metrics.to_csv("/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifySongsMetrics")
