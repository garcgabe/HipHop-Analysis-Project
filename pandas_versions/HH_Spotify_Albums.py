from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres
import pandas as pd

import sys, json

spot = SpotifyWrapper()
db = Postgres()
    
def fetch_data():

    artists_uri = pd.DataFrame(db.fetch_data(f"""
            SELECT artist_uri, spotify_name FROM artists;
            """), columns = ("artist_uri", "spotify_name")
    )
    # title of each column
    columns = ["album_uri", "album_name", "total_tracks", "release_date", 
            "artist_uris", "artist_names", "images"]
    
    print("Beginning album fetch...")
    # init empty lists to load then concat into DF
    album_uri, album_name, total_tracks, release_date, artist_uris, artist_names, images  = ([] for i in range (7))
    for i in range(0,len(artists_uri)):
        name_real = artists_uri["spotify_name"][i]
        print(f"Searching for albums by {name_real}...")
        name_uri = artists_uri["artist_uri"][i]
        search_tree = spot.getAlbums(name_uri)["items"]
        for _, search_tree_split in enumerate(search_tree):
            #print(search_tree_split)
            #sys.exit()
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
            

            json_string = json.dumps(search_tree_split, indent=4)
            #print(json_string)

            temp_album_uri = search_tree_split["uri"]
            album_uri.append(temp_album_uri)

            temp_album_name = search_tree_split["name"].strip().split("\n")[0].replace(",", "")
            album_name.append(temp_album_name)

            temp_total_tracks = str(search_tree_split["total_tracks"])
            total_tracks.append(temp_total_tracks)

            # if length is above 8 it has daily accuracy. if not, just yearly and we take the first date of it
            # NOTE: check this in data to see if it's only yearly and daily. monthly would need more logic
            temp_release_date = search_tree_split["release_date"] if len(search_tree_split["release_date"]) > 8 else search_tree_split["release_date"] + "-01-01"
            release_date.append(temp_release_date)

            # joining URIs by - for future parsing
            temp_artist_uris = "-".join(all_uris)
            artist_uris.append(temp_artist_uris)

            # joining URIs by - for future parsing
            temp_artist_names = "-".join(all_artists)
            artist_names.append(temp_artist_names)

            temp_images = search_tree_split["images"][0]["url"]
            images.append(temp_images)

            ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
            ## on conflict do nothing - album already accounted for by prior artist

            db.execute_query(f"""
                INSERT INTO albums (album_uri, album_name, total_tracks, release_date, artist_uris, artist_names, images)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (album_uri)
                    DO NOTHING
                """, (temp_album_uri, temp_album_name, temp_total_tracks, temp_release_date, temp_artist_uris, temp_artist_names, temp_images))


    ## final DF
    return pd.concat([pd.Series(album_uri), pd.Series(album_name), pd.Series(total_tracks),
                                        pd.Series(release_date), pd.Series(artist_uris), pd.Series(artist_names), pd.Series(images)], 
                                        axis=1, keys=columns)

if __name__=="__main__":
    album_data = fetch_data()
    # print(album_data.sort_values("album_uri"))
    
    # duplicates handled by shared album_uri --> do nothing if already in table
    # album_data = album_data.drop_duplicates(subset="album_uri", keep='first')
    
    # print(album_data.sort_values("album_uri"))


