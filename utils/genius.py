from utils.env import GENIUS_CLIENT_ID, GENIUS_CLIENT_SECRET, GENIUS_ACCESS_TOKEN
import lyricsgenius as lg

class Genius():
    def __init__(self):
        self.genius = lg.Genius(GENIUS_ACCESS_TOKEN)

    def getSongsByArtist(self, artist, number):
        return (self.genius.search_artist(artist, max_songs=number,get_full_info=False)).songs
    


    ## add way more of these to get all songs by album and shit
