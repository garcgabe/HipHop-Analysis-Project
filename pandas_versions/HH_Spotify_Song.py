from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres
import pandas as pd

# debugging
import sys, json

db = Postgres()
spot = SpotifyWrapper()

def call_data(all_albums):

    print("Fetching songs for: " + str(len(all_albums)) + " albums.")
    song_uri, song_name, album_uri, artist_names, explicit, preview_url = ([] for _ in range(6))
    columns = ["song_uri", "song_name", "album_uri", "artist_names", "explicit", "preview_url"]
    for counter in range(0,len(all_albums)):
        uri = all_albums.iloc[counter]["album_uri"]
        #print(counter, uri)
        if(counter%25 == 0):
            print("Album #: "+str(counter))
        
        # search on album URI   
        album_data = spot.getAlbumsTracks(uri)["items"]

        # temp arrays to hold multiple artist names
        temp_artists = []
        number_of_artists = len(album_data[0]["artists"])
        # search for cases where there are multiple artists and artist_uris
        # need to parse and add as a list instead of a single value
        for num in range(0,number_of_artists):
            artist_name_in_list = album_data[0]["artists"][num]["name"]
            temp_artists.append(artist_name_in_list.replace(",", ""))
        # join these lists into one variables to append to list for DF addition
        # each song within this loop iteration will share these 2 variables since same album
        album_artists = "-".join(temp_artists)

        # populate lists with song data
        for song_num in range(0,len(album_data)): 
            temp_song_uri =  album_data[song_num]["uri"]
            song_uri.append(temp_song_uri)

            name = album_data[song_num]["name"]
            temp_song_name = name.replace(",", "")
            song_name.append(temp_song_name)

            album_uri.append(uri)  
            artist_names.append(album_artists)

            #print(f"Song name: {name} by {artist_name_in_list}")
            temp_explicit = album_data[song_num]["explicit"]
            explicit.append(temp_explicit)

            temp_preview_url = album_data[song_num]["preview_url"]
            preview_url.append(temp_preview_url)

            # commit to DB
            ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
            ## on conflict do nothing - album already accounted for by prior artist

            db.execute_query(f"""
                INSERT INTO songs (song_uri, song_name, album_uri, artist_names, explicit, preview_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (song_uri)
                    DO NOTHING
                """, (temp_song_uri, temp_song_name, uri, album_artists, temp_explicit, temp_preview_url))

    # concatenate the lists 
    return pd.concat([pd.Series(song_uri), pd.Series(song_name), pd.Series(album_uri),
                                        pd.Series(artist_names), pd.Series(explicit), pd.Series(preview_url)], 
                                        axis=1, keys=columns)


if __name__ == "__main__":
    # Read from album table in DB
    spot_album_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT album_uri FROM albums;
            """), columns = ["album_uri"]
    )

    #actual fetch of songs into DB
    spot_songs = call_data(spot_album_uris)
    

