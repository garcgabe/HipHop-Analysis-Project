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

def _get_all_album_statistics(artist):
    album_response = supabase.table("albums")\
        .select("*, metrics(*)")\
        .like('artist_uris', f'%{artist_uri}%')\
        .execute()
    # convert all data to DF; then return
    return pd.DataFrame(album_response.data)
