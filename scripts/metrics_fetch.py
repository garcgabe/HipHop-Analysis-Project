# tools
import requests, base64, json
import pandas as pd
import numpy as np
import sys, time

# resources
from utils.env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from utils.postgres import Postgres

db = Postgres()

# can split this out into a utility later
def _token_client_credentials():
    # Encode the client ID and client secret
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    credentials_bytes = credentials.encode('ascii')
    base64_bytes = base64.b64encode(credentials_bytes)
    base64_credentials = base64_bytes.decode('ascii')
    
    response = requests.post('https://accounts.spotify.com/api/token',
                             headers = {
                                 'Authorization': f"Basic {base64_credentials}",
                                 'Content_Type': "application/x-www-form-urlencoded"
                             },
                             data = {'grant_type': 'client_credentials'}
                             )
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"Access Token received successfully.")#as: {token}")
        return token
    else:
        print(f"Failed request: {response.status_code}")


def _get_popularity(headers, song_uri_id):
        response = requests.get(f"https://api.spotify.com/v1/tracks/{song_uri_id}",
                                headers=headers
                                )
        if response.status_code == 429: 
            print(f"Triage {song_uri_id} at a later time; was called during rate limit")
            time.sleep(30)
        elif response.status_code != 200: print(f"Error getting request: {response.status_code}")
        else:
            json_obj = response.json()
            return json_obj["popularity"]


def _preprocess(songs_df: pd.DataFrame):
    return np.array_split(songs_df, np.ceil(len(songs_df) / 100)) 

def get_metrics(access_token: str, songs: pd.DataFrame):
    headers = {'Authorization' : f"Bearer {access_token}"}

    # split songs into sections of 100 for batch requests
    partitions = _preprocess(songs)

    for partition_index, partition in enumerate(partitions):
        print(f"Processing partition {partition_index} of {len(partitions)}")
        song_names = partition["song_name"]
        song_uris = partition["song_uri"]
        joined_uris = ','.join(uri for uri in song_uris)            

        if partition_index%5== 0: # reset access token periodically
            headers = {'Authorization' : f"Bearer {_token_client_credentials()}"}
        response = requests.get(f"https://api.spotify.com/v1/audio-features/{joined_uris}",
                                headers=headers
                                )
        if response.status_code == 429: 
            print(f"Triage partition {partition_index} at a later time; was called during rate limit")
            time.sleep(30)
        elif response.status_code != 200: print(f"Error getting request: {response.status_code}")
        else:
            print(json.dumps(response.json(), indent=4))
            json_obj = response.json()
            sys.exit(0)
                # duration_sec = json_obj['duration_ms'] * 0.001
                # popularity = _get_popularity(headers, uri_id)
                # danceability = json_obj['danceability']
                # energy = json_obj['energy']
                # loudness = json_obj['loudness']
                # valence = json_obj['valence']
                # tempo = json_obj['tempo']
                # instrumentalness = json_obj['instrumentalness']
                # speechiness = json_obj['speechiness']

                # db.execute_query(f"""
                #     INSERT INTO metrics (song_uri, song_name, duration, popularity, danceability, energy, loudness, valence, tempo, instrumentalness, speechiness)
                #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                #         ON CONFLICT (song_uri)
                #         DO NOTHING
                #     """, (uri, name, duration_sec, popularity, danceability, energy, loudness, valence, tempo, instrumentalness, speechiness))                                        
        db.close()


if __name__=="__main__":

    # Read from album table in DB
    songs = pd.DataFrame(db.fetch_data(f"""
            SELECT song_uri, song_name FROM songs;
            """), columns = ["song_uri", "song_name"]
    )
    access_token = _token_client_credentials()

    # extraction of metrics
    get_metrics(access_token, songs)




