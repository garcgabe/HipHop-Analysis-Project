# tools
import requests, base64, json
import pandas as pd
import sys, time

# resources
from utils.env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from utils.postgres import Postgres

db = Postgres()
# title of each column
columns = ["song_uri", "song_name", "album_uri", "artist_names", \
            "explicit", "preview_url"]

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


def get_songs_from_albums(access_token: str, album_uris: set):
    params = {
        "market" : "US",
        "limit" : 50
    }
    headers = {'Authorization' : f"Bearer {access_token}"}
    length = len(album_uris)
    for counter, uri in enumerate(album_uris):
        uri_id = uri.split(":")[-1] # API only takes ID not full URI
        # logging
        if counter%25 == 0: print(f"{counter} of {length}")
        response = requests.get(f"https://api.spotify.com/v1/albums/{uri_id}/tracks",
                                headers=headers, params=params
                                )
        if response.status_code == 429: 
            print(f"Cleanup! {uri}")
            time.sleep(30)
        elif response.status_code != 200: print(f"Error getting request: {response.status_code}")
        else:
            #print(json.dumps(response.json()["items"], indent=4))
            json_obj = response.json()["items"]
            # temp arrays to hold multiple artist names
            temp_artists = []
            number_of_artists = len(json_obj[0]["artists"])
            # search for cases where there are multiple artists and artist_uris
            # need to parse and add as a list instead of a single value
            for count in range(0,number_of_artists):
                artist_name_in_list = json_obj[0]["artists"][count]["name"]
                temp_artists.append(artist_name_in_list.replace(",", ""))

            # join these lists into one variables to append to list for DF addition
            # each song within this loop iteration will share these 2 variables since same album
            album_artists = "-".join(temp_artists)

            # populate lists with song data
            for song_count in range(0,len(json_obj)): 
                song_uri =  json_obj[song_count]["uri"]
                song_name = json_obj[song_count]["name"].replace(",", "")
                explicit = json_obj[song_count]["explicit"]
                preview_url = json_obj[song_count]["preview_url"]

                # commit to DB
                ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
                ## on conflict do nothing - album already accounted for by prior artist

                db.execute_query(f"""
                    INSERT INTO songs (song_uri, song_name, album_uri, artist_names, explicit, preview_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (song_uri)
                        DO NOTHING
                    """, (song_uri, song_name, uri, album_artists, explicit, preview_url))


if __name__=="__main__":
    # Read from album table in DB
    album_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT album_uri FROM albums;
            """), columns = ["album_uri"]
    )
    access_token = _token_client_credentials()

    # extraction of songs for storage into DB
    get_songs_from_albums(access_token, set(album_uris["album_uri"]))



