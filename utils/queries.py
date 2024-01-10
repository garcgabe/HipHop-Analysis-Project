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

def _get_top_songs(artist, number):
    filter_response = supabase.table("songs")\
        .select("song_name, metrics(popularity)")\
        .like('artist_names', f'%{artist}%')\
        .order("metrics(popularity)", desc=True)\
        .limit(number)\
        .execute()
    return [(x.get('song_name'), x.get('metrics').get('popularity')) for x in filter_response.data]


#def _get_popularity_distribution(artist):
    filter_response = supabase.table("metrics")\
        .select("popularity")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data
#def _get_energy_distribution(artist):
    filter_response = supabase.table("metrics")\
        .select("energy")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data

#def _get_emotion_distribution(artist):
    filter_response = supabase.table("metrics")\
        .select("valence")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data

#def _get_danceability_distribution(artist):
    filter_response = supabase.table("metrics")\
        .select("danceability")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data