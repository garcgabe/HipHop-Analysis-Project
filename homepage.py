import streamlit as st
import os
import pandas as pd
from supabase import create_client

from st_supabase_connection import SupabaseConnection


url = st.secrets["supabase_url"].SUPABASE_URL
key = st.secrets["supabase_key"].SUPABASE_KEY

supabase = create_client(url, key)

# querying all artists and info
response = supabase.table("artists").select("* limit 5").execute()

st.write(response + "\n\n\n")
st.write(response.data)

st.write(pd.DataFrame(data.json()))
st.write(count)
# # print
# for artist in artists:
#     st.write(f"{artist}")

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