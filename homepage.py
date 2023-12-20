import streamlit as st
from utils.postgres import Postgres

#db = Postgres(**st.secrets.aws_credentials)
conn = st.connection("postgresql", type="sql", 
                     **st.secrets.db_credentials)

# only gets artist names
artists = conn.query("""
            SELECT artist_uri, artist_name FROM artists
""")

# gets artist names - delimited by 
albums = conn.query("""
            SELECT album_uri, artist_uris
""")

## query to filter by artists
selected_artist_uri = None #add

filtered_album_uris = conn.query(f"""
            SELECT album_uri FROM albums
            WHERE artist_uris LIKE '%{selected_artist_uri}$'
""")



st.write(artists)

st.sidebar.markdown("rap analytics")

st.title("welcome to the rap analytics page")




st.image("")