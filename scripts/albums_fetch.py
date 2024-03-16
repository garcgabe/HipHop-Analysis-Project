# tools
import requests, base64, json
import pandas as pd
import sys

# resources
from utils.env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from utils.postgres import Postgres

db = Postgres()
# title of each column
columns = ["album_uri", "album_name", "total_tracks", "release_date", 
        "artist_uris", "artist_names", "images", "type"]

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


def fetch_album_data(access_token: str, artists_df):
    params = {
        "include_groups" : "album,single,appears_on"
    }
    headers = {'Authorization' : f"Bearer {access_token}"}

    # testing
    #artists_df =artists_df[:2]

    artist_names = list(artists_df["spotify_name"])
    artist_uris = list(artists_df["artist_uri"])

    for counter, (name, uri) in enumerate(zip(artist_names, artist_uris)):
        print(f"Searching for albums by {name}...")
        print(counter, name, uri)
        uri_id = uri.split(":")[-1] # API only takes ID not full URI

        response = requests.get(f"https://api.spotify.com/v1/artists/{uri_id}/albums",
                                headers=headers, params=params
                                )
        if response.status_code != 200: print(f"Error getting request: {response.status_code}")
        else:
            print(json.dumps(response.json()["items"], indent=4))
            json_obj = response.json()["items"]
            for _, json_tree_split in enumerate(json_obj):
                all_artists, all_uris = ([] for x in range(2))
                number_of_artists = len(json_tree_split["artists"])
                
                # for all artists, check if they exist in our list
                # if they do exist, we have their URI and can assign them to the album properly
                # if not, pass a 0 and keep their name for future addition if needed
                for artist_num in range(0,number_of_artists):
                    artist_name_in_list = json_tree_split["artists"][artist_num]["name"].replace(",", "")
                    try:
                        artist_uri_in_list = artists_df.loc[artists_df["spotify_name"] == artist_name_in_list, "artist_uri"].iloc[0]
                    except:
                        artist_uri_in_list = "0"
                    all_uris.append(artist_uri_in_list)
                    all_artists.append(artist_name_in_list)
                
                album_uri = json_tree_split["uri"]
                album_name = json_tree_split["name"].strip().split("\n")[0].replace(",", "")
                album_type = json_tree_split["album_type"]
                total_tracks = str(json_tree_split["total_tracks"])

                # if length is above 8 it has daily accuracy. if not, just yearly and we take the first date of it
                # NOTE: check this in data to see if it's only yearly and daily. monthly would need more logic
                release_date = json_tree_split["release_date"] if len(json_tree_split["release_date"]) > 8 \
                                                               else json_tree_split["release_date"] + "-01-01"
                # joining
                artist_uris = "-".join(all_uris)
                artist_names = "-".join(all_artists)
                images = json_tree_split["images"][0]["url"]

                ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
                ## on conflict do nothing - album already accounted for by prior artist

                db.execute_query(f"""
                    INSERT INTO albums (album_uri, album_name, total_tracks, release_date, artist_uris, artist_names, images, type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (album_uri)
                        DO NOTHING
                    """, (album_uri, album_name, total_tracks, release_date, artist_uris, artist_names, images, album_type))

            
if __name__=="__main__":
    artists = pd.DataFrame( db.fetch_data(f"""
    SELECT artist_uri, spotify_name FROM artists;
    """), columns = ("artist_uri", "spotify_name") )

    access_token = _token_client_credentials()

    fetch_album_data(access_token, artists)



