from utils.spotify import SpotifyWrapper
from utils.postgres import Postgres
import pandas as pd

# debugging
import sys, json

db = Postgres()
spot = SpotifyWrapper()

def call_data(all_albums, all_artists):
    seen_artists = {key: False for key in all_artists}
    print(all_albums)

    print("Fetching songs for: " + str(len(all_albums)) + " albums.")
    song_uri, song_name, album_uri, artist_names, explicit, preview_url = ([] for i in range(6))
    columns = ["song_uri", "song_name", "album_uri", "artist_names", "explicit", "preview_url"]
    for counter in range(0,len(all_albums)):
        uri = all_albums.iloc[counter]["album_uri"]
        print(counter, uri)
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
            seen_artists[artist_name_in_list] = True
            temp_artists.append(artist_name_in_list.replace(",", ""))
        # join these lists into one variables to append to list for DF addition
        # each song within this loop iteration will share these 2 variables since same album
        album_artists = "-".join(temp_artists)

        # populate lists with song data
        for song_num in range(0,len(album_data)):  
            song_uri.append(album_data[song_num]["uri"])

            name = album_data[song_num]["name"]
            song_name.append(name.replace(",", ""))

            album_uri.append(uri)  
            artist_names.append(album_artists)

            #print(f"Song name: {name} by {artist_name_in_list}")
            explicit.append(album_data[song_num]["explicit"])
            preview_url.append(album_data[song_num]["preview_url"])

    # concatenate the lists 
    song_df = pd.concat([pd.Series(song_uri), pd.Series(song_name), pd.Series(album_uri),
                                        pd.Series(artist_names), pd.Series(explicit), pd.Series(preview_url)], 
                                        axis=1, keys=columns)
    print(song_df.sort_values("song_name"))
    # pass DF through to get song metrics based on unique song_uri
    song_df = song_df.sort_values("explicit", ascending=False)
    return song_df.drop_duplicates(subset="song_uri", keep='first')


if __name__ == "__main__":
    #CHANGE to read from Dim Artist and Dim Albums
    spot_album_uris = pd.DataFrame(db.fetch_data(f"""
            SELECT album_uri FROM albums;
            """), columns = ["album_uri"]
    )
    spot_album_uris = spot_album_uris[:10]

    # get artist names and uris to add to song data
    spot_artist_names = pd.DataFrame(db.fetch_data(f"""
            SELECT artist_uri, spotify_name FROM artists;
            """), columns = ("artist_uri", "spotify_name")
    )

    #actual fetch of songs into dataframe
    spot_songs = call_data(spot_album_uris, spot_artist_names)
    
    print(spot_songs.sort_values("song_name"))
    # spot_songs.to_csv("/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifySongs")

