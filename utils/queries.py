from supabase import create_client
import streamlit as st
import pandas as pd

url = st.secrets["supabase_url"].SUPABASE_URL
key = st.secrets["supabase_key"].SUPABASE_KEY

supabase = create_client(url, key)

def _get_artists():
    response = supabase.table("artists")\
        .select("artist_name")\
        .execute()
    return [x.get('artist_name') for x in response.data]

def _get_artist_info(artist):
    filter_response = supabase.table("artists")\
        .select("*")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return pd.DataFrame(filter_response.data)

def _get_albums(artist_uri):
    album_response = supabase.table("albums")\
        .select("*")\
        .like('artist_uris', f'%{artist_uri}%')\
        .execute()
    # convert all data to DF; then return
    return pd.DataFrame(album_response.data)

def _get_top_songs(artist, number):
    filter_response = supabase.table("songs")\
        .select("song_name, metrics(popularity)")\
        .like('artist_names', f'%{artist}%')\
        .order("metrics(popularity)", desc=True)\
        .limit(number)\
        .execute()
    return [(x.get('song_name'), x.get('metrics').get('popularity')) for x in filter_response.data]


def _get_distribution(artist, column):
    filter_response = supabase.table("songs")\
        .select(f"metrics({column})")\
        .like('artist_names', f'%{artist}%')\
        .execute()
    results = [x.get('metrics').get(f'{column}') for x in filter_response.data]
    return (min(results), sum(results)/len(results), max(results))

def _get_all_song_statistics(artist_uri):
    rows_list = []

    album_response = supabase.table("albums")\
        .select("album_name, metrics(song_name, popularity, danceability, energy, valence)")\
        .like('artist_uris', f'%{artist_uri}%')\
        .execute()
    all_album_data = album_response.data

    # enumerate through album LIST, each album is dict
    for idx, album in enumerate(all_album_data):
        album_name = {"album_name": album.get('album_name')}
        metrics = album.get('metrics')
        # # enumerate through song LIST, each song is dict of metrics
        for song_idx, song_metrics in enumerate(metrics):
            new_row = album_name.copy()
            new_row.update(song_metrics)
            rows_list.append(new_row)

    # reorder for viewing
    return_df = pd.DataFrame(rows_list)
    return return_df[["song_name", "album_name", "popularity", "danceability", "energy", "valence"]]
