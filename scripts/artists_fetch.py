# tools
import requests, base64, json

# resources
from utils.env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from utils.postgres import Postgres
from utils.constants import artists


# title of each column
columns = ["artist_uri", "artist_name", "spotify_name", 
            "popularity", "followers",
            "genres", "images"]

db = Postgres()

# can split this out into a utility later
def _token_client_credentials():
    # Encode the client ID and client secret
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    credentials_bytes = credentials.encode('ascii')
    base64_bytes = base64.b64encode(credentials_bytes)
    base64_credentials = base64_bytes.decode('ascii')
    
    response = requests.post('https://accounts.spotify.com/api/token',
                             headers = {
                                 'Authorization': f"Basic {base64_credentials}",
                                 'Content_Type': "application/x-www-form-urlencoded"
                             },
                             data = {'grant_type': 'client_credentials'}
                             )
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"Access Token received successfully.")#as: {token}")
        return token
    else:
        print(f"Failed request: {response.status_code}")


def fetch_artist_data(access_token: str):
    params = {
        "q" : None,
        "type" : "artist",
        "market" : "US",
        "limit" : 1
    }
    headers = {'Authorization' : f"Bearer {access_token}"}
    

    for counter, artist in enumerate(artists):
       # if counter%5==0: 
        print(counter, artist)
        params["q"]=artist

        response = requests.get("https://api.spotify.com/v1/search",
                                headers=headers, params=params
                                )
        if response.status_code != 200: 
            print(f"Error getting request: {response.status_code}") 
            return
        #print(json.dumps(response.json()))
        json_obj = response.json()["artists"]["items"][0]
        #print(json_obj)
        artist_uri = json_obj["uri"]
        artist_name = artist.replace(",", "")
        spotify_name = json_obj["name"].replace(",", "")
        popularity = json_obj["popularity"]
        followers = json_obj["followers"]["total"]
        genres = "-".join([_ for _ in json_obj["genres"]])
        images = json_obj["images"][0]["url"]
        
        # performs an UPSERT for the artist information
        db.execute_query(f"""
            INSERT INTO artists (artist_uri, artist_name, spotify_name, popularity, followers, genres, images)
                   VALUES (%s, %s, %s,%s, %s, %s, %s)
                   ON CONFLICT (artist_uri)
                   DO UPDATE SET popularity = EXCLUDED.popularity, followers = EXCLUDED.followers, genres = EXCLUDED.genres, images = EXCLUDED.images
            """, (artist_uri, artist_name, spotify_name, popularity, followers, genres, images))
        ## the conflict above is if the same artist is being added 
        ## we used EXCLUDED.col to bring in the new data
    db.close()


if __name__=="__main__":
    access_token = _token_client_credentials()
    fetch_artist_data(access_token)



