import lyricsgenius as lg
import pandas as pd

fetch_number = 1
artists = []

class geniusWrapper():
    genius_client_id = '6ik7FFRHyv94azwRfLlDIpTAS-710CM1BoWDfO2x82LkpIz9g9Oo5-YQbp_B_xzA'
    genius_client_secret = '23fPMx4U0q6TJRT0ss3aIpXRhT9w0taLUf-3_w2iRxAYU1b3uKSPvucwdqbkf8iObaqM5-_f0RXOTV92bLeLvQ'

    def __init__(self):
        self.genius = lg.Genius('SFSvR6r7o3-3g123P0DUAFkiqsvBZaptEbjQw2Nw6rAPLUkUA9d89_8VdNa9tK50')
 
    def getSongsByArtist(self, artist, number):
        return (self.genius.search_artist(artist, max_songs=number,get_full_info=False)).songs

def clean_string(name):
    cleaned = name.replace('\'','').replace('\n','').replace('’', '')
    return cleaned

def readArtists():
    artists = []
    with open('artists.txt') as file:
        name = 'x'
        while(name != ''):
            name = file.readline()
            if name.strip() and 'stop' not in name:
                artists.append(name.split("\n")[0])  
            else:
                break
    return artists


def call_data(artists):
    genius = geniusWrapper()
    columns = ['artist_name', 'song','popularity_index', 'pageviews']
    artist_names, songs, popularity_index, views = ([] for i in range(4) )
    for artist in artists:
        print(f"Working on {artist}")
        successfulGet = 0
        while successfulGet != 1:
            try:
                pop_index = 1 
                songs_search = genius.getSongsByArtist(artist, fetch_number)
                for song_number in range(0, fetch_number):
                    artist_names.append(artist)
                    popularity_index.append(pop_index)
                    song = songs_search[song_number]
                    songs.append( clean_string(song.title) )
                    try:
                        views.append( song.stats.pageviews )
                    except:
                        views.append(0)
                    pop_index += 1
                print(f"Ending song extraction for {artist}")
                successfulGet=1
            except:
                print("failed...")
    extracted_songs = pd.concat([pd.Series(artist_names),pd.Series(songs), 
                        pd.Series(popularity_index), pd.Series(views)], 
                        axis=1, keys=columns)
    return extracted_songs

if __name__ == "__main__":
    artists = readArtists()
    dataframe = call_data(artists)
    print(dataframe)
    #dataframe.to_excel("GeniusData.xlsx")