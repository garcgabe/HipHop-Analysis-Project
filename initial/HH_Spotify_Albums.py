from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres
import pandas as pd

import sys, json

spot = SpotifyWrapper()
db = Postgres()
    
def get_album_data(artists):
    print("Beginning album fetch...")

    # title of each column
    columns = ["album_uri", "album_name", "total_tracks", "release_date", 
            "artist_uris", "artist_names", "images"]

    for artist_count in range(0,len(artists)):
        name_real = artists["spotify_name"][artist_count]
        print(f"Searching for albums by {name_real}...")

        name_uri = artists["artist_uri"][artist_count]
        search_tree = spot.getAlbums(name_uri)["items"]

        for _, search_tree_split in enumerate(search_tree):
            all_artists, all_uris = ([] for x in range(2))
            number_of_artists = len(search_tree_split["artists"])
            
            # for all artists, check if they exist in our list
            # if they do exist, we have their URI and can assign them to the album properly
            # if not, pass a 0 and keep their name for future addition if needed
            for artist_num in range(0,number_of_artists):
                artist_name_in_list = search_tree_split["artists"][artist_num]["name"].replace(",", "")
                try:
                    artist_uri_in_list = artists_uri.loc[artists_uri["spotify_name"] == artist_name_in_list, "artist_uri"].iloc[0]
                except:
                    artist_uri_in_list = "0"
                all_uris.append(artist_uri_in_list)
                all_artists.append(artist_name_in_list)
            
            album_uri = search_tree_split["uri"]
            album_name = search_tree_split["name"].strip().split("\n")[0].replace(",", "")
            total_tracks = str(search_tree_split["total_tracks"])

            # if length is above 8 it has daily accuracy. if not, just yearly and we take the first date of it
            # NOTE: check this in data to see if it's only yearly and daily. monthly would need more logic
            release_date = search_tree_split["release_date"] if len(search_tree_split["release_date"]) > 8 else search_tree_split["release_date"] + "-01-01"
            # joining
            artist_uris = "-".join(all_uris)
            artist_names = "-".join(all_artists)
            images = search_tree_split["images"][0]["url"]

            ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
            ## on conflict do nothing - album already accounted for by prior artist

            db.execute_query(f"""
                INSERT INTO albums (album_uri, album_name, total_tracks, release_date, artist_uris, artist_names, images)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (album_uri)
                    DO NOTHING
                """, (album_uri, album_name, total_tracks, release_date, artist_uris, artist_names, images))

if __name__=="__main__":
    artists_uri = pd.DataFrame(db.fetch_data(f"""
        SELECT artist_uri, spotify_name FROM artists;
        """), columns = ("artist_uri", "spotify_name")
    )

    get_album_data(artists_uri)