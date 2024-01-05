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


album_response = supabase.table("albums")\
    .select("*")\
    .like('artist_uris', f'%{selected_artist_uri}%')\
    .execute()
# convert all data to DF; then 
album_result = pd.DataFrame(album_response.data)

albums = pd.dataframe(album_result)
st.dataframe(albums)



# column layout
col1, col2 = st.columns([1,2])  # Adjust the column widths as needed
col1.image(selected_artist_image, width=200)
col2.dataframe(result,\
    # column_config={
    #     "images": st.column_config.ImageColumn("image", width=50)
    # },
    )

# TODO: bring in album metrics
#        - number of albums
#
#
# 
#
#

## query to filter by artists

# filtered_album_uris = conn.query(f"""
#             SELECT album_uri FROM albums
#             WHERE artist_uris LIKE '%{selected_artist_uri}$'
# """)



st.title("welcome to the rap analytics page")

