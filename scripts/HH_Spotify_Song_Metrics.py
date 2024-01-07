import pandas as pd
import time, sys, json

from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres

db = Postgres()
spot = SpotifyWrapper()

def get_song_metrics(uris):
    """
    Extracts audio features for a list of songs and loads to DB
    
    Parameters:
        uris (pd DF): 2 columns: song_uri, song_name
    
    Returns:
        None, loads DB
    """
    total_songs = len(uris)
    print(f"Fetching audio features for {total_songs} songs.")

    columns = ["song_uri", "song_name", "duration_sec", "popularity", "danceability", "energy", "loudness", "valence", \
        "tempo", "instrumentalness","speechiness"]
    for count in range(0,total_songs):
        if(count%50 == 0):
            print("Song # "+str(count)+" of "+ str(total_songs ))
    
        song_uri = uris.iloc[count]["song_uri"]
        song_name = uris.iloc[count]["song_name"]

        try:
            audio_features = spot.getAudioFeatures(song_uri)
            track_data = spot.getTrack(song_uri)
        except:
            print("Too many requests. Sleeping...")
            time.sleep(60)
        
        if (not audio_features or not track_data):
            print(f"{song_name} not found. skipping...")
            continue
        else:
            duration_sec = track_data['duration_ms'] * 0.001
            popularity = track_data['popularity']

            danceability = audio_features[0]['danceability']
            energy = audio_features[0]['energy']
            loudness = audio_features[0]['loudness']
            valence = audio_features[0]['valence']
            tempo = audio_features[0]['tempo']
            instrumentalness = audio_features[0]['instrumentalness']
            speechiness = audio_features[0]['speechiness']

            db.execute_query(f"""
                INSERT INTO metrics (song_uri, song_name, duration_sec, popularity, danceability, energy, loudness, valence, tempo, instrumentalness, speechiness)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (song_uri)
                    DO NOTHING
                """, (song_uri, song_name, duration_sec, popularity, danceability, energy, loudness, valence, tempo, instrumentalness, speechiness))                                        

if __name__=="__main__":
    # Read from album table in DB
    song_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT song_uri, song_name FROM songs;
            """), columns = ["song_uri", "song_name"]
    )
    
    get_song_metrics(song_uris)

