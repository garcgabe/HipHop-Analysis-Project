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
        .select("song_name, popularity")\
        .eq('artist_name', f'{artist}')\
        .order("popularity", ascending=False)\
        .limit(number)\
        .execute()
    print(f"DEBUG:{filter_response.data}")
    return [(x.get('song_name'), x.get('popularity')) for x in filter_response.data]

def _get_popularity_distribution(artist):
    filter_response = supabase.table("songs")\
        .select("popularity")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data

def _get_energy_distribution(artist):
    filter_response = supabase.table("songs")\
        .select("energy")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data

def _get_emotion_distribution(artist):
    filter_response = supabase.table("songs")\
        .select("valence")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data

def _get_danceability_distribution(artist):
    filter_response = supabase.table("songs")\
        .select("danceability")\
        .eq('artist_name', f'{artist}')\
        .execute()
    return filter_response.data