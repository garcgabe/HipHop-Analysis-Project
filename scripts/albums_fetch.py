# tools
import requests, base64, json
import pandas as pd
import sys

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
    # 3 of the same image at various sizes; take first
    image = json_obj["images"][0]["url"]
    
    # performs an insert for new artist information
    db.execute_query(f"""
        INSERT INTO artists (artist_uri, artist_name, popularity, followers, genres, images)
                VALUES (%s, %s, %s,%s, %s, %s)
                ON CONFLICT (artist_uri)
                DO UPDATE SET popularity = EXCLUDED.popularity, followers = EXCLUDED.followers, genres = EXCLUDED.genres, images = EXCLUDED.images
        """, (uri, artist_name, popularity, followers, genres, image))
    return (uri, artist_name)


def fetch_album_data(access_token: str, artists_df) -> None:
    params = {
        "include_groups" : "album,single,appears_on",
        "market" : "US",
        "limit" : 50
    }
    headers = {'Authorization' : f"Bearer {access_token}"}

    # testing
    #artists_df =artists_df[:2]

    artist_names = list(artists_df["artist_name"])
    artist_uris = list(artists_df["artist_uri"])

    # separate set for checking if the have data for the given artist URI
    # new artist URIs will be found in helper function and added to -artists- table
    artist_uri_check = set(artists_df["artist_uri"])
    for counter, (name, uri) in enumerate(zip(artist_names, artist_uris)):
        print(f"Searching for albums by {name}...")
        print(counter, name, uri)
        uri_id = uri.split(":")[-1] # API only takes ID not full URI
        response = requests.get(f"https://api.spotify.com/v1/artists/{uri_id}/albums",
                                headers=headers, params=params
                                )
        if response.status_code != 200: print(f"Error getting request: {response.status_code}")

        #print(json.dumps(response.json()["items"], indent=4))
        #sys.exit(0)
        json_obj = response.json()["items"]
        for item in json_obj:
            album_uri = item["uri"]
            album_name = item["name"].strip().split("\n")[0].replace(",", "")
            album_type = item["album_type"]

            # if length is above 8 it has daily accuracy. if not, just yearly and we take the first date of it
            # NOTE: check this in data to see if it's only yearly and daily. monthly would need more logic
            release_date = item["release_date"] if len(item["release_date"]) > 8 \
                                                else item["release_date"] + "-01-01"
            total_tracks = str(item["total_tracks"])
            images = item["images"][0]["url"]

            ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
            ## on conflict do nothing - album already accounted for by prior artist

            db.execute_query(f"""
                INSERT INTO albums (album_uri, album_name, type, release_date, total_tracks, images)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (album_uri)
                    DO NOTHING
                """, (album_uri, album_name, album_type, release_date, total_tracks, images))
            
            # OUTER: add to album_artist relation table
            # INNER: add artist if they're not seen yet
            # first add to memory set (for future checking); then persist
            for artist in item["artists"]:
                insertion = (uri, name) #base case is base artist
                temp_uri = artist["uri"]
                if temp_uri not in artist_uri_check:
                    # add new URI to in-mem set
                    artist_uri_check.add(temp_uri)
                    # persist to DB in artists list; return artist tuple
                    insertion = _add_new_artist(access_token, temp_uri)
                #insert alum/artist relation
                db.execute_query(f"""
                    INSERT INTO album_artists (album_uri, artist_uri, album_name, artist_name)
                        VALUES(%s, %s, %s, %s)
                        ON CONFLICT (album_uri, artist_uri)
                        DO NOTHING
                    """, (album_uri, insertion[0], album_name, insertion[1]))
    db.close()
            
if __name__=="__main__":
    artists = pd.DataFrame( db.fetch_data(f"""
    SELECT artist_uri, artist_name FROM artists;
    """), columns = ("artist_uri", "artist_name") )

    #print(artists)
    access_token = _token_client_credentials()
    #uzi_test_df = pd.DataFrame([{"artist_uri":"spotify:artist:4O15NlyKLIASxsJ0PrXPfz", "artist_name":"Lil Uzi Vert"}] ,columns=("artist_uri", "artist_name"))
    #print(uzi_test_df)
    #fetch_album_data(access_token, uzi_test_df)
    fetch_album_data(access_token, artists)
    


