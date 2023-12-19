import streamlit as st
from utils.postgres import Postgres

db = Postgres()

# only gets artist names
artists = db.fetch_data("""
            SELECT artist_uri, artist_name FROM artists
""")

# gets artist names - delimited by 
albums = db.fetch_data("""
            SELECT album_uri, artist_uris
""")

st.write(artists)

st.sidebar.markdown("rap analytics")

st.title("welcome to the rap analytics page")




st.image("")