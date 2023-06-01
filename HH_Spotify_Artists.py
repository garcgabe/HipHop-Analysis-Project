import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

class spotWrapper():
    def __init__(self):
        client_id = 'accd0aa479164ddcbf1cbf822512b80b'
        client_secret = '58bfc467435045e7b61c86fb03385729'
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
            "spotify_followers","genres", "image"]
    # init empty lists to load then concat into DF
    artist_name, spotify_name, artist_uri, genres, spotify_popularity, spotify_followers, images  = ([] for i in range (7))

    for i in range(0,len(artists)):
        # for each Name from Genius, search under artists and return data 
        search_name = artists[i]
        if(i%5==0):
            print(f"{i}: {search_name}")
        search_name_tree = spot.searchArtist(search_name)['artists']['items'][0]

        artist_name.append(search_name)
        spotify_name.append(search_name_tree["name"])
        artist_uri.append(search_name_tree["uri"])
        genres.append(search_name_tree["genres"])
        spotify_popularity.append(search_name_tree["popularity"])
        spotify_followers.append(search_name_tree["followers"]["total"])
        images.append(search_name_tree["images"][0]["url"])

    return pd.concat([pd.Series(artist_name), pd.Series(spotify_name), pd.Series(artist_uri),
                                        pd.Series(spotify_popularity), pd.Series(spotify_followers), pd.Series(genres), pd.Series(images)], 
                                        axis=1, keys=columns)
    
if __name__=="__main__":
    df = fetch_artists()
    # just until loaded into SQL
    df.to_excel("SpotifyArtists.xlsx")
    print(df)
