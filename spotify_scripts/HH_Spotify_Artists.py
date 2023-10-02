from utils.spotify import SpotifyWrapper
import pandas as pd

# Artists brought in from constant list
from utils.constants import artists

spot = SpotifyWrapper()
 
def fetch_artists():
    print("Beginning artist fetch...")

    # title of each column
    columns = ["artist_uri", "artist_name", "spotify_name", 
               "spotify_popularity", "spotify_followers",
               "genres", "images"]
    
    # init empty lists to load then concat into DF
    artist_name, spotify_name, artist_uri, genres, spotify_popularity, spotify_followers, images  = ([] for i in range (7))

    for counter, search_name in enumerate(artists):
        # for each Name from Genius, search under artists and return data 
        if(counter%5==0):
            print(counter, search_name)
        
        search_name_tree = spot.searchArtist(search_name)['artists']['items'][0]

        artist_name.append(search_name.replace(",", ""))
        spotify_name.append(search_name_tree["name"].replace(",", ""))
        artist_uri.append(search_name_tree["uri"])
        genres.append("-".join([_ for _ in search_name_tree["genres"]]) )
        spotify_popularity.append(search_name_tree["popularity"])
        spotify_followers.append(search_name_tree["followers"]["total"])
        images.append(search_name_tree["images"][0]["url"])

    return pd.concat([pd.Series(artist_uri), pd.Series(artist_name), pd.Series(spotify_name),
                                        pd.Series(spotify_popularity), pd.Series(spotify_followers), 
                                        pd.Series(genres), pd.Series(images)], 
                                        axis=1, keys=columns)
    
if __name__=="__main__":
    df = fetch_artists()
    print(df)
    df.index.name = "artist_id"
    # just until loaded into SQL



    df.to_csv("/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifyArtists")
    print(df)
