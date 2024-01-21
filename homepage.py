import streamlit as st
import os
import pandas as pd
from utils import queries
from utils import pareto_card
from supabase import create_client
from streamlit_extras.metric_cards import style_metric_cards

###################################################
# get all artist options from DB
artists = queries._get_artists()

# SELECT ARTIST FROM FRONTEND
selected_name = st.selectbox("select an artist", options=artists)

# get selected artist's info
result = queries._get_artist_info(selected_name)

# identify image and uri we will use going ahead
selected_artist_image = result.loc[result['artist_name'] == selected_name]['images'][0]
selected_artist_uri = result.loc[result['artist_name'] == selected_name]['artist_uri'][0]
selected_artist_genres = result.loc[result['artist_name'] == selected_name]['genres'][0].split("-")

# remove uri and image from data table
result = result.drop(['artist_uri','images'], axis=1)

#card = pareto_card.generate(selected_name, selected_artist_genres, selected_artist_image)
# st.markdown(card[0], unsafe_allow_html=True)
# st.markdown(card[1], unsafe_allow_html=True)

st.markdown("""
    <style>
    .container { text-align: center; justify-content: center; margin-bottom: 10px; }
    </style>
""")
st.markdown(f"""
<body>
    <div class="container">
        <img src={selected_artist_image} width="300" height="300"></img>
    </div>
</body>
""")

st.divider()
# column layout
col1, col2 = st.columns([1,1])  # Adjust the column widths as needed
selection = result.loc[result['artist_name'] == selected_name]
col1.metric('popularity', selection['popularity'][0])
col2.metric('followers', f"{int(selection['followers'][0]):,}")
st.metric('genres', \
    ", ".join(genre for genre in selection['genres'][0].split('-')),\
        )
style_metric_cards(background_color="#000000",
    border_size_px = 0,
    border_color= "#9AD8E1",
    border_radius_px = 0,
    border_left_color = "#9AD8E1",
    box_shadow= False)

#
#
###########################################
###               ALBUM DATA            ###
###########################################
#
#

# get all album data for artist
album_result = queries._get_albums(selected_artist_uri)

# reordering columns for visualization
album_result = album_result[['images', 'album_uri', 'artist_uris', 'artist_names', 'album_name', 'release_date', 'total_tracks']]

st.dataframe(album_result.drop(['album_uri', 'artist_uris'], axis=1),
    column_config={
        "images": st.column_config.ImageColumn("image", width=50)
    },
)


album_uris = list(album_result['album_uri'])
#
#
###########################################
###               SONG DATA             ###
###########################################
#
#
st.markdown("<h1>Album Breakdown</h1>", unsafe_allow_html=True)
# TODO: bring in album metrics
#        - number of albums
#
#
# 
#
#




