import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import psycopg2 as pg
import sys

class spotWrapper():
    def __init__(self):
        client_id = 'accd0aa479164ddcbf1cbf822512b80b'
        client_secret = '58bfc467435045e7b61c86fb03385729'
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    def getAlbums(self, uri):
        return self.spot.artist_albums(uri, album_type="album")
    

    
def connect():
    connection_var = pg.connect(
        host="localhost",
        database="hiphop",
        user="garcgabe",
        password="password"
    )
    return connection_var



def create_df():
    spot = spotWrapper()
###
### these need to change to read artist info from the DB
###
    spot_artists = pd.read_excel("/Users/garcgabe/Desktop/HipHop-Analysis-Project/SpotifyArtists.xlsx").drop("Unnamed: 0", axis=1)
    artists_uri = spot_artists[['spotify_name','artist_uri']]
    # title of each column
    columns = ["album_uri", "album_name", "total_tracks", "release_date", 
            "artist_uris", "artist_names"]

    # init empty lists to load then concat into DF
    album_uri, album_name, total_tracks, release_date, artist_uris, artist_names  = ([] for i in range (6))
    for i in range(0,len(artists_uri)-25):
        name_uri = artists_uri["artist_uri"][i]
        search_tree = spot.getAlbums(name_uri)['items']
        for j in range(0,len(search_tree)):
            search_tree_split = search_tree[j]
            #print(search_tree_split.keys())
            #sys.exit()
            all_artists, all_uris = ([] for x in range(2))
            number_of_artists = len(search_tree_split["artists"])
            for artist_num in range(0,number_of_artists):
                artist_name_in_list = search_tree_split["artists"][artist_num]["name"]
                try:
                    artist_uri_in_list = spot_artists.loc[spot_artists["spotify_name"] == artist_name_in_list, "artist_uri"].iloc[0]
                except:
                    artist_uri_in_list = "0"
                all_uris.append(artist_uri_in_list)
                all_artists.append(artist_name_in_list)
            artist_names.append(", ".join(all_artists))
            artist_uris.append(", ".join(all_uris))
            album_uri.append(search_tree_split["uri"])
            album_name.append(search_tree_split["name"].strip().split("\n")[0])
            total_tracks.append(str(search_tree_split["total_tracks"]))
            release_date.append(search_tree_split["release_date"])
    ## final DF
    return pd.concat([pd.Series(album_uri), pd.Series(album_name), pd.Series(total_tracks),
                                        pd.Series(release_date), pd.Series(artist_uris), pd.Series(artist_names)], 
                                        axis=1, keys=columns)

if __name__=="__main__":
    album_data = create_df()
    album_data.to_excel("SpotifyAlbums.xlsx")
    print(album_data)