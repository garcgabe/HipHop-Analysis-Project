import streamlit as st
import requests

from st_supabase_connection import SupabaseConnection

url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]

st.write(url)
st.write(key)

resp = requests.get(url, api_key=key)
st.write(resp.status_code, )

# st.write(artists)
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