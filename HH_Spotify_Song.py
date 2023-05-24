import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from fuzzywuzzy import fuzz

class spotWrapper():
    def __init__(self):
        client_id = 'accd0aa479164ddcbf1cbf822512b80b'
        client_secret = '58bfc467435045e7b61c86fb03385729'
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def getAlbumsTracks(self, id):
        return self.spot.album_tracks(id)
    def getAudioFeatures(self, song_uri):
        return self.spot.audio_features(song_uri)

def clean_string(name):
    cleaned = name.replace('\'','').replace('\n','').replace('’', '')
    return cleaned
    


def call_data(all_albums, all_artists):
    spot = spotWrapper()

    print("getting songs for: " + str(len(all_albums)) + " albums.")
    song_uri, song_name, album_uri, artist_uris, artist_names, explicit, preview_url = ([] for i in range(7))
    columns = ["song_uri", "song_name", "album_uri", "artist_uris", "artist_names", "explicit", "preview_url"]
    counter = 0
    for idx in all_albums:
        # search on album URI   
        print("Album number "+ str(counter) )
        counter+=1
        if(counter > 100):
            break
        album_data = spot.getAlbumsTracks(idx)["items"]
        number_of_artists = len(album_data[0]["artists"])
        for num in range(0,number_of_artists):
            artist_name_in_list = album_data[0]["artists"][num]["name"]
            try:
                artist_uri_in_list = all_artists.loc[all_artists["spotify_name"] == artist_name_in_list, "artist_uri"].iloc[0]
            except:
                artist_uri_in_list = "0"


        for song_num in range(0,len(album_data)):  
            album_uri.append(idx)  
            artist_uris.append(artist_uri_in_list)
            artist_names.append(artist_name_in_list)
            song_uri.append(album_data[song_num]["uri"])
            name = album_data[song_num]["name"]
            song_name.append(name)
            #print(f"Song name: {name} by {artist_name_in_list}")
            explicit.append(album_data[song_num]["explicit"])
            preview_url.append(album_data[song_num]["preview_url"])




    song_df = pd.concat([pd.Series(song_uri), pd.Series(song_name), pd.Series(album_uri),pd.Series(artist_uris),
                                        pd.Series(artist_names), pd.Series(explicit), pd.Series(preview_url)], 
                                        axis=1, keys=columns)
    song_df.to_excel("interm_songs.xlsx")
    return add_song_metrics(song_df)




def add_song_metrics(df):
    dance, energy, loudness, valence, tempo, instru, speech = ([] for i in range(7))

    spot = spotWrapper()
    for i in range(0, len(df)):
        song_uri = df.loc[i]["song_uri"]
        spot_audio = spot.getAudioFeatures(song_uri)

        dance.append(spot_audio[0]['danceability'])
        energy.append(spot_audio[0]['energy'])
        loudness.append(spot_audio[0]['loudness'])
        valence.append(spot_audio[0]['valence'])
        tempo.append(spot_audio[0]['tempo'])
        instru.append(spot_audio[0]['instrumentalness'])
        speech.append(spot_audio[0]['speechiness'])

    # Add arrays of song characteristics into main DataFrame
    df['dance'] = dance
    df['energy'] = energy
    df['loudness'] = loudness
    df['valence'] = valence
    df['tempo'] = tempo
    df['instru'] = instru
    df['speech'] = speech
    return df  

if __name__ == "__main__":
    #CHANGE to read from Dim Artist and Dim Albums
    album_df = pd.read_excel("SpotifyAlbums.xlsx")
    artist_df = pd.read_excel("SpotifyArtists.xlsx")

    spot_artist_names = artist_df[["spotify_name", "artist_uri"]]
    spot_album_uris = album_df["album_uri"]
    spot_songs = call_data(spot_album_uris, spot_artist_names)

    print(spot_songs.head() )
    #spot_songs.to_excel("SpotifySongs.xlsx")

