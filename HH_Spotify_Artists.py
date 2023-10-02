import pandas as pd

# Spotify Wrapper object to fetch
from utils.spotify import SpotifyWrapper
# Artists brought in from constant list
from utils.constants import artists
# Postgres class to execute queries
from utils.postgres import Postgres

db = Postgres()
spot = SpotifyWrapper()
 
def fetch_data():
    print("Beginning artist fetch...")

    # title of each column
    columns = ["artist_uri", "artist_name", "spotify_name", 
               "popularity", "followers",
               "genres", "images"]
    
    # init empty lists to load then concat into DF
    artist_name, spotify_name, artist_uri, genres, popularity, followers, images  = ([] for i in range (7))

    for counter, search_name in enumerate(artists):
        # for each Name from Genius, search under artists and return data 
        if(counter%5==0):
            print(counter, search_name)
        
        search_name_tree = spot.searchArtist(search_name)['artists']['items'][0]

        temp_artist_uri = search_name_tree["uri"]
        artist_uri.append(temp_artist_uri)

        temp_artist_name = search_name.replace(",", "")
        artist_name.append(temp_artist_name)

        temp_spotify_name = search_name_tree["name"].replace(",", "")
        spotify_name.append(temp_spotify_name)

        temp_popularity = search_name_tree["popularity"]
        popularity.append(temp_popularity)

        temp_followers = search_name_tree["followers"]["total"]
        followers.append(temp_followers)

        temp_genres = "-".join([_ for _ in search_name_tree["genres"]])
        genres.append(temp_genres)

        temp_images = search_name_tree["images"][0]["url"]
        images.append(temp_images)


        # performs an UPSERT for the artist information
        db.execute_query(f"""
            INSERT INTO artists (artist_uri, artist_name, spotify_name, popularity, followers, genres, images)
                   VALUES (%s, %s, %s,%s, %s, %s, %s)
                   ON CONFLICT (artist_uri)
                   DO UPDATE SET popularity = EXCLUDED.popularity, followers = EXCLUDED.followers, genres = EXCLUDED.genres, images = EXCLUDED.images
            """, (temp_artist_uri, temp_artist_name, temp_spotify_name, temp_popularity, temp_followers, temp_genres, temp_images))
        ## the conflict above is if the same artist is being added 
        ## we used EXCLUDED.col to bring in the new data

    # return dataframe for debugging if needed
    return pd.concat([pd.Series(artist_uri), pd.Series(artist_name), pd.Series(spotify_name),
                                        pd.Series(popularity), pd.Series(followers), 
                                        pd.Series(genres), pd.Series(images)], 
                                        axis=1, keys=columns)
    
if __name__=="__main__":
    artist_data = fetch_data()

