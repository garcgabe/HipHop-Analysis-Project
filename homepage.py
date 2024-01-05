import streamlit as st
import os
import pandas as pd
from supabase import create_client

from st_supabase_connection import SupabaseConnection


url = st.secrets["supabase_url"].SUPABASE_URL
key = st.secrets["supabase_key"].SUPABASE_KEY

supabase = create_client(url, key)

###################################################
# get artist options from DB
response = supabase.table("artists")\
    .select("artist_name")\
    .execute()
artists = [x.get('artist_name') for x in response.data]

# SELECT ARTIST FROM FRONTEND
selected_name = st.selectbox("select an artist", \
    options=artists)

# querying all artists and info
filter_response = supabase.table("artists")\
    .select("*")\
    .eq('artist_name', f'{selected_name}')\
    .execute()

# convert all data to DF; then 
result = pd.DataFrame(filter_response.data)

# identify image and uri we will use going ahead
selected_artist_image = result.loc[result['artist_name'] == selected_name]['images'][0]
selected_artist_uri = result.loc[result['artist_name'] == selected_name]['artist_uri'][0]

# remove uri and image from data table
result = result.drop(['artist_uri','images'], axis=1)

st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="center"><img src="{selected_artist_image}" width="200"></div>',
    unsafe_allow_html=True
)

# column layout
col1, col2 = st.columns([1,1])  # Adjust the column widths as needed
selection = result.loc[result['artist_name'] == selected_name]
# col1.metric('popularity!', selection['popularity'][0])
# col2.metric('followers!', selection['followers'][0])
# st.metric('genres!', \
#     ", ".join(genre for genre in selection['genres'][0].split('-')),\
#         )
col1.markdown(
    '<div class="center"><h2>popularity!</h2><p>{}</p></div>'.format(selection['popularity'][0]),
    unsafe_allow_html=True
)

col2.markdown(
    '<div class="center"><h2>followers!</h2><p>{}</p></div>'.format(selection['followers'][0]),
    unsafe_allow_html=True
)

st.markdown(
    '<div class="center"><h2>genres!</h2><p>{}</p></div>'.format(", ".join(genre for genre in selection['genres'][0].split('-'))),
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="display: flex; justify-content: space-between;">
        <div style="width: 33%; text-align: left;">
            <h3>Top Left</h3>
        </div>
        <div style="width: 33%; text-align: right;">
            <h3>Top Right</h3>
        </div>
    </div>
    <div style="width: 100%; text-align: center;">
        <h3>Centered</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# col2.dataframe(result.drop('spotify_name', axis=1),\
#     # column_config={
#     #     "images": st.column_config.ImageColumn("image", width=50)
#     # },
#     )


###########################################
###               ALBUM DATA            ###
###########################################

album_response = supabase.table("albums")\
    .select("*")\
    .like('artist_uris', f'%{selected_artist_uri}%')\
    .execute()
# convert all data to DF; then 
album_result = pd.DataFrame(album_response.data)
# reordering columns
album_result = album_result[['images', 'album_uri', 'artist_uris', 'artist_names', 'album_name', 'release_date', 'total_tracks']]

st.dataframe(album_result.drop(['album_uri', 'artist_uris'], axis=1),
    column_config={
        "images": st.column_config.ImageColumn("image", width=50)
    },
)

album_uris = list(album_result['album_uri'])
###########################################
###               SONG DATA             ###
###########################################



# TODO: bring in album metrics
#        - number of albums
#
#
# 
#
#




