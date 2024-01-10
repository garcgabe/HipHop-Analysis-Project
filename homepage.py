import streamlit as st
import os
import pandas as pd
from utils import queries
from supabase import create_client
from streamlit_extras.metric_cards import style_metric_cards

##
def _generate_genre_html(genres):
  genre_html = "<h5>"
  number_genres = len(selected_artist_genres)
  if number_genres <= 2:
      genre_html += " --- ".join(selected_artist_genres)
  elif(number_genres <=6):
      for i in range(0, number_genres, 2):
          genre_html += " --- ".join(selected_artist_genres[i:i+2])
          genre_html += "<br>"
  else:
      for i in range(0, 6, 2):
        genre_html += " --- ".join(selected_artist_genres[i:i+2])
        genre_html += "<br>"
  genre_html += "</h5>"
  return genre_html

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

genre_html = _generate_genre_html(selected_artist_genres)

topsongs = queries._get_top_songs(selected_name, 5)
popularity_distribution = queries._get_distribution(selected_name, 'popularity')
dance_distribution = queries._get_distribution(selected_name, 'danceability')
emotion_distribution = queries._get_distribution(selected_name, 'valence')
energy_distribution = queries._get_distribution(selected_name, 'energy')    

st.markdown("""
<style>
  body { font-family: Helvetica, sans-serif; }
  .container { display: flex; }
  .card { width: 300px; height: 500px; border: 2px solid #AAA; 
   background-image: linear-gradient(to bottom right, #133832, #552506);
    border-image: linear-gradient(to right, #F1E1A4, #FFFFFF);
    border-image-slice: 1;
    background-radius: 15px;
    flex:1
    }
  .card-header { text-align: center; justify-content: center; }
  .card-content { text-align: center; justify-content: center; margin-bottom: 10px; }
  .artist_pic { width:275px; height:275px; border-radius:50%; justify-content: center;}
  .front_info { font-family: Helvetica, sans-serif; word-wrap: break-word; max-width: 350px; margin: 0 auto;}
  h4{margin-top: 0; margin-bottom: 0; bottom: 0}
  p{margin-top: 0; margin-bottom: 0; }
  .top-songs {
    display: flex;
    flex-direction: column;
  }
  .song {
    display: flex;
    justify-content: space-between;
    padding-left: 10px;
  }
  .title {
    text-align: left;
  }
  .popularity {
    text-align: right;
    padding-right: 10px;
  }
  .metrics { text-align: bottom; }
  .metric { margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<body>
<div class="container"> 
<div class="card">
  <div class="card-header">
    <h3>{selected_name}</h3>
  </div>
  <div class="card-content">
    <img src="{selected_artist_image}" class = "artist_pic">
    <div class="front_info">
      {genre_html}
      <h6>◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍</h6>
      <h4>Pareto Score:   30%</h4>
    </div>
  </div>
</div>

<div class="card">
    <div class="card-header">
        <h3>Artist Top 5</h3>
    </div>
    <div class="card-content">
      <div class="top-songs">
        <div class="song">
          <span class="title">{topsongs[0][0]}</span>
          <span class="popularity">{topsongs[0][1]}</span>
        </div>
        <div class="song">
          <span class="title">{topsongs[1][0]}</span>
          <span class="popularity">{topsongs[1][1]}</span>
        </div>
        <div class="song">
          <span class="title">{topsongs[2][0]}</span>
          <span class="popularity">{topsongs[2][1]}</span>
        </div>
        <div class="song">
          <span class="title">{topsongs[3][0]}</span>
          <span class="popularity">{topsongs[3][1]}</span>
        </div>
        <div class="song">
          <span class="title">{topsongs[4][0]}</span>
          <span class="popularity">{topsongs[4][1]}</span>
        </div>
      </div>
      <h6>◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍</h6 >
      <div class="metrics">
        <div class="metric"><strong>Popularity</strong> {" - ".join(str(x) for x in popularity_distribution)}</div>
        <div class="metric"><strong>Energy</strong>{" - ".join(str(x) for x in energy_distribution)}</div>
        <div class="metric"><strong>Danceability</strong>{" - ".join(str (x) for x in dance_distribution)}</div>
        <div class="metric"><strong>Emotion</strong>{" - ".join(str(x) for x in emotion_distribution)}</div>
      </div>
    </div>
</div>
</div>

</body>
""", unsafe_allow_html=True)

# # centered artist image
# st.markdown(
#     """
#     <style>
#     .center {
#         display: flex;
#         justify-content: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown(
#     f'<div class="center"><img src="{selected_artist_image}" width="300"></div>',
#      unsafe_allow_html=True
# )

st.divider()
# column layout
col1, col2 = st.columns([1,1])  # Adjust the column widths as needed
selection = result.loc[result['artist_name'] == selected_name]
col1.metric('popularity!', selection['popularity'][0])
col2.metric('followers!', f"{int(selection['followers'][0]):,}")
st.metric('genres!', \
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

# TODO: bring in album metrics
#        - number of albums
#
#
# 
#
#




