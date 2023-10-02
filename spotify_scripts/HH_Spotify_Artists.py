import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

class spotWrapper():
    def __init__(self):
        client_id = '####'
        client_secret = '####'
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    def searchArtist(self, string):
        return self.spot.search(q=string, type="artist")
 
def readArtists():
    artists = []
    with open('/Users/garcgabe/Desktop/HipHop-Analysis-Project/artists.txt') as file:
        name = 'x'
        while(name != ''):
            name = file.readline()
            if name.strip() and 'stop' not in name:
                artists.append(name.split("\n")[0])  
            else:
                break
    return artists

def fetch_artists():
    print("Beginning artist fetch...")
    spot = spotWrapper()
    artists = readArtists()

    # title of each column
    columns = ["artist_name", "spotify_name", "artist_uri", "spotify_popularity", 
            "spotify_followers","genres", "images"]
    # init empty lists to load then concat into DF
    artist_name, spotify_name, artist_uri, genres, spotify_popularity, spotify_followers, images  = ([] for i in range (7))

    for i, search_name in enumerate(artists):
        # for each Name from Genius, search under artists and return data 
        if(i%5==0):
            print(i, search_name)
        search_name_tree = spot.searchArtist(search_name)['artists']['items'][0]

        artist_name.append(search_name.replace(",", ""))
        spotify_name.append(search_name_tree["name"].replace(",", ""))
        artist_uri.append(search_name_tree["uri"])
        genres.append("-".join([_ for _ in search_name_tree["genres"]]) )
        spotify_popularity.append(search_name_tree["popularity"])
        spotify_followers.append(search_name_tree["followers"]["total"])
        images.append(search_name_tree["images"][0]["url"])

    return pd.concat([pd.Series(artist_name), pd.Series(spotify_name), pd.Series(artist_uri),
                                        pd.Series(spotify_popularity), pd.Series(spotify_followers), 
                                        pd.Series(genres), pd.Series(images)], 
                                        axis=1, keys=columns)
    
if __name__=="__main__":
    df = fetch_artists()
    df.index.name = "artist_id"
    # just until loaded into SQL
    df.to_csv("/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifyArtists")
    print(df)
