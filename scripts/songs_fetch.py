# tools
import requests, base64, json
import pandas as pd
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

def _add_new_artist(access_token, uri) -> tuple:
    headers = {'Authorization' : f"Bearer {access_token}"}
    uri_id = uri.split(":")[-1] # API only takes ID not full URI
    response = requests.get(f"https://api.spotify.com/v1/artists/{uri_id}",
                            headers=headers
                            )
    if response.status_code != 200: 
        print(f"Error getting request for adding new artist: {response.status_code}") 
        return
    #print(json.dumps(response.json(), indent=4))
    json_obj = response.json()
    artist_name = json_obj["name"].replace(",", "")
    print(f"adding {artist_name}")
    popularity = json_obj["popularity"]
    followers = json_obj["followers"]["total"]
    genres = "-".join([_ for _ in json_obj["genres"]])
    try:
    # 3 of the same image at various sizes; take first
        image = json_obj["images"][0]["url"]
    except: image = ""
    
    # performs an insert for new artist information
    db.execute_query(f"""
        INSERT INTO artists (artist_uri, artist_name, popularity, followers, genres, images)
                VALUES (%s, %s, %s,%s, %s, %s)
                ON CONFLICT (artist_uri)
                DO UPDATE SET popularity = EXCLUDED.popularity, followers = EXCLUDED.followers, genres = EXCLUDED.genres, images = EXCLUDED.images
        """, (uri, artist_name, popularity, followers, genres, image))
    return (uri, artist_name)

def get_songs_from_albums(access_token: str, album_uris: set, artist_check: set):
    params = {
        "market" : "US",
        "limit" : 50
    }
    headers = {'Authorization' : f"Bearer {access_token}"}
    length = len(album_uris)
    for counter, uri in enumerate(album_uris):
        uri_id = uri.split(":")[-1] # API only takes ID not full URI
        # logging
        if counter%25 == 0: print(f"{counter} of {length} albums")
        response = requests.get(f"https://api.spotify.com/v1/albums/{uri_id}/tracks",
                                headers=headers, params=params
                                )
        if response.status_code == 429: 
            print(f"Triage {uri} at a later time; was called during rate limit")
            time.sleep(30)
        elif response.status_code != 200: print(f"Error getting request: {response.status_code}")
        else:
            #print(json.dumps(response.json()["items"], indent=4))
            json_obj = response.json()["items"]

            # populate lists with song data
            for song in json_obj: 
                #print(json.dumps(song, indent=4))
                song_uri =  song["uri"]
                song_name = song["name"].replace(",", "")
                explicit = song["explicit"]
                preview_url = song["preview_url"]

                ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
                ## on conflict do nothing - song already accounted for
                db.execute_query(f"""
                    INSERT INTO songs (song_uri, song_name, album_uri, explicit, preview_url)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (song_uri)
                        DO NOTHING
                    """, (song_uri, song_name, uri, explicit, preview_url))
                # OUTER: add to album_artist relation table
                # INNER: add artist if they're not seen yet
                # first add to memory set (for future checking); then persist
                for artist in song["artists"]:
                    temp_artist_uri = artist["uri"]
                    if temp_artist_uri not in artist_check:
                        # add new URI to in-mem set
                        artist_check.add(temp_artist_uri)
                        # persist to DB in artists list; return artist tuple
                        _add_new_artist(access_token, temp_artist_uri)
                    #insert song/artist relation
                    db.execute_query(f"""
                        INSERT INTO song_artists (song_uri, artist_uri, song_name, artist_name)
                            VALUES(%s, %s, %s, %s)
                            ON CONFLICT (song_uri, artist_uri)
                            DO NOTHING
                        """, (song_uri, artist["uri"], song_name, artist["name"]))
    db.close()


if __name__=="__main__":

    artist_uris = pd.DataFrame( db.fetch_data(f"""
    SELECT artist_uri, artist_name FROM artists;
    """), columns = ("artist_uri", "artist_name") )

    # Read from album table in DB
    album_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT album_uri FROM albums;
            """), columns = ["album_uri"]
    )
    access_token = _token_client_credentials()

    # extraction of songs for storage into DB
    get_songs_from_albums(access_token, set(album_uris["album_uri"]), set(artist_uris["artist_uri"]))
    #get_songs_from_albums(access_token, set(["spotify:album:0fEO7g2c5onkaXsybEtuD2", \
    #                                         "spotify:album:48xpWR8K6CGpy3ETAym3pt"]),
    #                      set(artist_uris["artist_uri"]))



