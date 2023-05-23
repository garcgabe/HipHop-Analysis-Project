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
    def search(self, string):
        return self.spot.search(q=string)

    def getTrack(self, song, artist):
        return self.spot.search(q=str(song + ' ' + artist))
    def getAudioFeatures(self, song_id):
        return self.spot.audio_features(song_id)

def get_fuzz_ratio(var1, var2):
    return fuzz.ratio(var1, var2)

def clean_string(name):
    cleaned = name.replace('\'','').replace('\n','').replace('’', '')
    return cleaned
    


def call_data(df):
    spot = spotWrapper()
    spot_names, spot_artists, ids, problem_songs = ([] for i in range(4))

    ## OPTIMIZE: check if there are parentheses - if so, split and take first token - then run fuzz scripts
    fuzz_song_threshold = 50 # fuzz_song is average of ratio and partial ratio
    fuzz_artist_threshold = 80


    for i in df.index:
        artist = df.loc[i]['Artist']
        song = df.loc[i]['Song']
        spot_name = None
        song_artist = None
        print(f"searching {song} {artist}")

    #Search Spotify for song + artist
        search_count = 0
        found = 0
        while( found < 1 and search_count < 3):
            track = spot.getTrack(song, artist)
            try: 
                spot_name = track['tracks']['items'][search_count]['name']
                song_artist = track['tracks']['items'][search_count]['album']['artists'][0]['name']

            except:
                print(f"{song} NOT SEARCHED SUCCESSFULLY at track var")
                problem_songs.append(f"{song} by {artist}")
                spot_names.append('NA')
                spot_artists.append('NA')
                ids.append('NA')
                found = 1
            
            fuzz_song = get_fuzz_ratio(song, spot_name)
            fuzz_partial = fuzz.partial_ratio(song, spot_name)
            song_fuzz = (fuzz_song + fuzz_partial) / 2

            fuzz_artist = get_fuzz_ratio(artist, song_artist)

            # DEBUG
            #print(f"Fuzz artist: {fuzz_artist} AND Fuzz song: {song_fuzz}")
            #print(f"{spot_name} by {song_artist} in SPOTIFY")

            # Good Case
            if ( fuzz_artist > fuzz_artist_threshold and song_fuzz > fuzz_song_threshold):
                spot_artists.append(song_artist)
                spot_names.append(clean_string(spot_name))
                ids.append(track['tracks']['items'][0]['id'])
                search_count = 3
                found = 1

            # Not Found and not in top 3 search results
            elif(found < 1 and search_count == 2):
                print(f"{song} by {artist} not found.")
                problem_songs.append(f"{song} by {artist}")
                spot_names.append('NA')
                spot_artists.append('NA')
                ids.append('NA')

            search_count +=1

    # Save Not-Found Songs to troubleshoot later
    problem_songs_df = pd.DataFrame(problem_songs)
    problem_songs_df.to_excel("Problem_Songs.xlsx")
    # Helper function to 
    SpotData_Fuzz = create_spotify_dataframe(spot_names, spot_artists, df['Artist'], df['Song'], ids)
    return add_song_metrics(SpotData_Fuzz)


def create_spotify_dataframe(spotify_songs, spotify_artists, genius_artists, genius_songs, song_ids):
    spot_data = pd.DataFrame()
    spot_data['Song_ID'] = song_ids
    spot_data['Spot_Song'] = spotify_songs
    spot_data['Spot_Artist'] = spotify_artists
    spot_data['Genius_Artist'] = genius_artists
    spot_data['Genius_Song'] = genius_songs

    fuzz_ratio_song, fuzz_ratio_artist, fuzz_ratio_partial_song = ([] for i in range(3))

    ## OPTIMIZE: combine for loops -- at each record, take 4 entries then compute on them
    for i in range(0,len(genius_songs)):
        #Song Fuzz
        real_song= spot_data.loc[i]['Genius_Song']
        found_song = spot_data.loc[i]['Spot_Song'] 
        fuzz_ratio_song.append(fuzz.ratio(real_song, found_song))
        fuzz_ratio_partial_song.append(fuzz.partial_ratio(real_song, found_song))

        # Artist Fuzz
        real_name= spot_data.loc[i]['Genius_Artist']
        found_name = spot_data.loc[i]['Spot_Artist'] 
        fuzz_ratio_artist.append(fuzz.ratio(real_name, found_name))
        
    spot_data['fuzz_song'] = fuzz_ratio_song
    spot_data['fuzz_artist'] = fuzz_ratio_artist
    spot_data['fuzz_partial_song'] = fuzz_ratio_partial_song 

    return spot_data 


def add_song_metrics(df):
    popularity, dance, energy, loudness, valence, tempo, instru, speech = ([] for i in range(8))

    spot = spotWrapper()
    missing = 0
    for i in range(0, len(df)):
        name = df.loc[i]['Spot_Song'][:18]
        artist = df.loc[i]['Spot_Artist']
        if name != 'NA':
            song_id = df.loc[i]['Song_ID']
            ## DEBUG print(f"Getting info for {name}")
            track = spot.getTrack(name, artist)
            pop = track['tracks']['items'][0]['popularity']
            popularity.append(pop)

            #
            spot_audio = spot.getAudioFeatures(song_id)
            dance.append(spot_audio[0]['danceability'])
            energy.append(spot_audio[0]['energy'])
            loudness.append(spot_audio[0]['loudness'])
            valence.append(spot_audio[0]['valence'])
            tempo.append(spot_audio[0]['tempo'])
            instru.append(spot_audio[0]['instrumentalness'])
            speech.append(spot_audio[0]['speechiness'])

            #
        # Song is not found on Spotify; likely Soundcloud only and not on streaming services
        # Handle by adding 0 to song characteristics to filter out later
        else: 
            popularity.append(0)
            dance.append(0)
            energy.append(0)
            loudness.append(0)
            valence.append(0)
            tempo.append(0)
            instru.append(0)
            speech.append(0)
            # Prints song name if it is not here
            missing += 1
            print(str(missing) + ' Missing Info: ' + df.loc[i]['Genius_Song'])
    # Add arrays of song characteristics into main DataFrame
    df['popularity'] = popularity
    df['dance'] = dance
    df['energy'] = energy
    df['loudness'] = loudness
    df['valence'] = valence
    df['tempo'] = tempo
    df['instru'] = instru
    df['speech'] = speech
    return df  

if __name__ == "__main__":
    //print("fix")
    #CHANGE to read from Dim Artist
    #genius_dataframe = pd.read_excel("GeniusData.xlsx")
   # spotify_dataframe = call_data(genius_dataframe)
   # spotify_dataframe.to_excel("SpotifyData.xlsx")

