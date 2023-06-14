import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time, sys


class spotWrapper():
    def __init__(self):
        # Hide these within venv variables
        client_id = 'accd0aa479164ddcbf1cbf822512b80b'
        client_secret = '58bfc467435045e7b61c86fb03385729'
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager,
                                    retries=10, status_retries=10)

    def getAlbumsTracks(self, id):
        return self.spot.album_tracks(id)
    def getAudioFeatures(self, song_uri):
        return self.spot.audio_features(song_uri)


def call_data(all_albums, all_artists):
    spot = spotWrapper()
    print("Fetching songs for: " + str(len(all_albums)) + " albums.")
    song_uri, song_name, album_uri, artist_uris, artist_names, explicit, preview_url = ([] for i in range(7))
    columns = ["song_uri", "song_name", "album_uri", "artist_uris", "artist_names", "explicit", "preview_url"]
    for counter, idx in enumerate(all_albums):
        if(counter%25 == 0):
            print("Album #: "+str(counter))
        # search on album URI   
        album_data = spot.getAlbumsTracks(idx)["items"]
        # temp arrays to hold multiple artist names and their uris
        temp_artists, temp_artist_uris = ([] for x in range(2))
        number_of_artists = len(album_data[0]["artists"])
        # search for cases where there are multiple artists and artist_uris
        # need to parse and add as a list instead of a single value
        for num in range(0,number_of_artists):
            artist_name_in_list = album_data[0]["artists"][num]["name"]
            try:
                artist_uri_in_list = all_artists.loc[all_artists["spotify_name"] == artist_name_in_list, "artist_uri"].iloc[0]
            except:
                artist_uri_in_list = "0"
            temp_artists.append(artist_name_in_list.replace(",", ""))
            temp_artist_uris.append(artist_uri_in_list)
        # join these lists into one variables to append to list for DF addition
        # each song within this loop iteration will share these 2 variables since same album
        album_artists = "-".join(temp_artists)
        album_artist_uris = "-".join(temp_artist_uris)

        # populate lists with song data
        for song_num in range(0,len(album_data)):  
            album_uri.append(idx)  
            artist_uris.append(album_artist_uris)
            artist_names.append(album_artists)
            song_uri.append(album_data[song_num]["uri"])
            name = album_data[song_num]["name"]
            song_name.append(name.replace(",", ""))
            #print(f"Song name: {name} by {artist_name_in_list}")
            explicit.append(album_data[song_num]["explicit"])
            preview_url.append(album_data[song_num]["preview_url"])

    # concatenate the lists 
    song_df = pd.concat([pd.Series(song_uri), pd.Series(song_name), pd.Series(album_uri),pd.Series(artist_uris),
                                        pd.Series(artist_names), pd.Series(explicit), pd.Series(preview_url)], 
                                        axis=1, keys=columns)
    # pass DF through to get song metrics based on unique song_uri
    return song_df


if __name__ == "__main__":
    #CHANGE to read from Dim Artist and Dim Albums

    # get album_uris to search for songs
    album_df = pd.read_csv("S3 Data/SpotifyAlbums")
    spot_album_uris = album_df["album_uri"]
    # get artist names and uris to add to song data
    artist_df = pd.read_csv("S3 Data/SpotifyArtists")
    spot_artist_names = artist_df[["spotify_name", "artist_uri"]]

    #actual fetch of songs into dataframe
    spot_songs = call_data(spot_album_uris, spot_artist_names)

    #persist dataframe in excel
    #spot_songs.to_excel("SpotifySongs.xlsx")
    spot_songs.index.name = "index"
    print(spot_songs)
    spot_songs.to_csv("/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifySongs")

