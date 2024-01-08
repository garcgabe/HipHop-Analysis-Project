import streamlit as st
import os
import pandas as pd
from supabase import create_client
from streamlit_extras.metric_cards import style_metric_cards

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
selected_artist_genres = result.loc[result['artist_name'] == selected_name]['genres'][0].split("-")

# remove uri and image from data table
result = result.drop(['artist_uri','images'], axis=1)

card_front, card_back = st.columns([1,1])

card_front.markdown("""
<style>
  body { font-family: Arial, sans-serif; }
  .card { width: 300px; height: 500px; border: 2px solid #AAA; border-radius: 10px; padding: 10px; }
  .card-header { text-align: center; justify-content: center; }
  .card-content { display: flex; justify-content: center; position: relative; }
  .artist_pic { width:300px; height:300px; border-radius:50%; padding: 25px }
  .genres { text-align: bottom; }

  .dotted-line {width: 100%; height: 2px; border-bottom: 2px dotted #CCC; padding: 25px; }
  .card-top5 {}
  .metrics { text-align: bottom; }
  .metric { margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

card_front.markdown(f"""
<div class="card">
  <div class="card-header">
    <h3>{selected_name}</h3>
    <img src="{selected_artist_image}" class = "artist_pic">
    <p>{"---".join(genre for genre in selected_artist_genres)}</p>
  
  <div class="dotted-line"><p>                   </p></div>
    <p>Pareto Score</p>
    <p>30%</p>
  </div>
  </div>
""", unsafe_allow_html=True)


topsongs = ['Artist1', 'Artist2', 'Artist3', 'Artist4', 'Artist5']


card_back.markdown(f"""
  <div class="card">
    <div>
      <p>{topsongs[0]} - 91</p>
      <p>{topsongs[1]} - 86%</p>
      <p>{topsongs[2]} - 88%</p>
      <p>{topsongs[3]} - 87%</p>
      <p>{topsongs[4]} - 79%</p>
    </div>
    <div class="dots-line">
    </div>

    <div class="metrics">
      <div class="metric"><strong>Popularity</strong> 50 - 75 - 90</div>
      <div class="metric"><strong>Danceability</strong> 20 - 70 - 90</div>
      <div class="metric"><strong>Emotion</strong> 20 - 60 - 80</div>
    </div>
  </div>
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




