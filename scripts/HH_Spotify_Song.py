from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres
import pandas as pd
# debugging
import sys, json

db = Postgres()
spot = SpotifyWrapper()

def get_songs_from_albums(albums):
    """
        Retrieves songs from Spotify using a list of albums and inserts them into DB

        Parameters:
            albums (pandas.DataFrame): A single column pandas DF containing unique album identifiers.

        Returns:
            None
    """
    print("Fetching songs for: " + str(len(albums)) + " albums.")

    columns = ["song_uri", "song_name", "album_uri", "artist_names", "explicit", "preview_url"]

    for counter in range(0,len(albums)):
        album_uri = albums.iloc[counter]["album_uri"]

        if(counter%25 == 0):
            print("Album #: "+str(counter))
        
        # search on album URI   
        album_data = spot.getAlbumsTracks(album_uri)["items"]

        # temp arrays to hold multiple artist names
        temp_artists = []
        number_of_artists = len(album_data[0]["artists"])
        # search for cases where there are multiple artists and artist_uris
        # need to parse and add as a list instead of a single value
        for count in range(0,number_of_artists):
            artist_name_in_list = album_data[0]["artists"][count]["name"]
            temp_artists.append(artist_name_in_list.replace(",", ""))

        # join these lists into one variables to append to list for DF addition
        # each song within this loop iteration will share these 2 variables since same album
        album_artists = "-".join(temp_artists)

        # populate lists with song data
        for song_count in range(0,len(album_data)): 
            song_uri =  album_data[song_count]["uri"]
            song_name = album_data[song_count]["name"].replace(",", "")
            explicit = album_data[song_count]["explicit"]
            preview_url = album_data[song_count]["preview_url"]

            # commit to DB
            ## NOTE: this data is static, therefore on conflicts we do nothing to the existing rows
            ## on conflict do nothing - album already accounted for by prior artist

            db.execute_query(f"""
                INSERT INTO songs (song_uri, song_name, album_uri, artist_names, explicit, preview_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (song_uri)
                    DO NOTHING
                """, (song_uri, song_name, album_uri, album_artists, explicit, preview_url))

if __name__ == "__main__":
    # Read from album table in DB
    album_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT album_uri FROM albums;
            """), columns = ["album_uri"]
    )

    # extraction of songs for storage into DB
    get_songs_from_albums(album_uris)
    

