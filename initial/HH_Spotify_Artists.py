import pandas as pd

# Spotify Wrapper object to fetch
from utils.spotify import SpotifyWrapper
# Artists brought in from constant list
from utils.constants import artists
# Postgres class to execute queries
from utils.postgres import Postgres

db = Postgres()
spot = SpotifyWrapper()
 
def get_artist_data():
    """
    Fetches artist data from Spotify and inserts it into DB.

    Parameters: 
        None, but artist list is set as a constant

    Returns:
        None
    """

    print("Beginning artist fetch...")

    # title of each column
    columns = ["artist_uri", "artist_name", "spotify_name", 
               "popularity", "followers",
               "genres", "images"]
    
    for counter, search_name in enumerate(artists):
        # for each Name from Genius, search under artists and return data 
        if(counter%5==0):
            print(counter, search_name)
        
        search_name_tree = spot.searchArtist(search_name)['artists']['items'][0]

        artist_uri = search_name_tree["uri"]
        artist_name = search_name.replace(",", "")
        spotify_name = search_name_tree["name"].replace(",", "")
        popularity = search_name_tree["popularity"]
        followers = search_name_tree["followers"]["total"]
        genres = "-".join([_ for _ in search_name_tree["genres"]])
        images = search_name_tree["images"][0]["url"]

        # performs an UPSERT for the artist information
        db.execute_query(f"""
            INSERT INTO artists (artist_uri, artist_name, spotify_name, popularity, followers, genres, images)
                   VALUES (%s, %s, %s,%s, %s, %s, %s)
                   ON CONFLICT (artist_uri)
                   DO UPDATE SET popularity = EXCLUDED.popularity, followers = EXCLUDED.followers, genres = EXCLUDED.genres, images = EXCLUDED.images
            """, (artist_uri, artist_name, spotify_name, popularity, followers, genres, images))
        ## the conflict above is if the same artist is being added 
        ## we used EXCLUDED.col to bring in the new data
    
if __name__=="__main__":
    get_artist_data()

