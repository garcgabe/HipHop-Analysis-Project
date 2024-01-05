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
    .select("artist_name, popularity, followers, genres, images")\
    .eq('artist_name', f'{selected_name}')\
    .execute()
filter_query_result = pd.DataFrame(filter_response.data)

st.table(filter_query_result)

# only gets artist names
# artists = conn.query("""
#             SELECT artist_uri, artist_name FROM artists
# """)

# gets artist names - delimited by 
# albums = conn.query("""
#             SELECT album_uri, artist_uris
# """)

## query to filter by artists
# selected_artist_uri = None #add

# filtered_album_uris = conn.query(f"""
#             SELECT album_uri FROM albums
#             WHERE artist_uris LIKE '%{selected_artist_uri}$'
# """)



#st.write(artists)

st.sidebar.markdown("rap analytics")

st.title("welcome to the rap analytics page")




#st.image("")