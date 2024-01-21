import streamlit as st
import os
import pandas as pd
from utils import queries
from utils import pareto_card
from supabase import create_client


# did not end up using; took code for own usage below
#from streamlit_extras.metric_cards import style_metric_cards

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

selection = result.loc[result['artist_name'] == selected_name]
popularity = selection['popularity'][0]
followers = f"{int(selection['followers'][0]):,}"
genre_list =  ", ".join(genre for genre in selection['genres'][0].split('-'))


#card = pareto_card.generate(selected_name, selected_artist_genres, selected_artist_image)
# st.markdown(card[0], unsafe_allow_html=True)
# st.markdown(card[1], unsafe_allow_html=True)

st.markdown("""
    <style>
    .container { text-align: center; justify-content: center; margin-bottom: 5px; }
    .metric_holder { background-color: #000000;
                border: 2px solid #9AD8E1;
                padding: 5%;
                border-radius: 2px;
                border-left: 0.5rem solid #9AD8E1;}
    .metric { display: flex; justify-content: space-between; padding-left: 5px;}

    .metric_label { text-align: left; font-size: 20px; font-weight: bold; color: #9AD8E1; padding-left: 20px;}
    .metric_value { text-align: right; padding-right: 20px; color: white; font-size: 16px}

    .song { display: flex; justify-content: space-between; padding-left: 10px;}
    .title {text-align: left; }
    .popularity { text-align: right; padding-right: 10px; }
    .metrics { text-align: bottom; }
    .metric { padding-left: 30px; pading-right: 30px; margin-bottom: 5px; }
    h6 { color: #9AD8E1; font-size: 20px; font-weight: bold; }

    </style>
""", unsafe_allow_html=True)
st.markdown(f"""
<body>
    <div class="container">
        <img src={selected_artist_image} width="300" height="300"></img>
    </div>
    <div class="container">
        <div class="metric_holder">
          <div class="metric">
            <span class="metric_label">followers:</span>
            <span class="metric_value">{followers}</span>
          </div>
          <div class="metric">
            <span class="metric_label">popularity:</span>
            <span class="metric_value">{popularity}</span>
          </div>
          <div class="metric">
            <span class="metric_label">genres:</span>
            <span class="metric_value">{genre_list}</span>
          </div>
        </div>
</body>
""", unsafe_allow_html=True)

st.divider()

topsongs = queries._get_top_songs(selected_name, 5)
popularity_distribution = queries._get_distribution(selected_name, 'popularity')
dance_distribution = queries._get_distribution(selected_name, 'danceability')
emotion_distribution = queries._get_distribution(selected_name,'valence')
energy_distribution = queries._get_distribution(selected_name, 'energy') 

st.markdown(f"""
<body>
    <div class="container">
        <div class="metric_holder">
            <div class="song">
                <span class="metric_label">{topsongs[0][0]}</span>
                <span class="popularity">{topsongs[0][1]}</span>
            </div>
            <div class="song">
                <span class="metric_label">{topsongs[1][0]}</span>
                <span class="popularity">{topsongs[1][1]}</span>
            </div>
            <div class="song">
                <span class="metric_label">{topsongs[2][0]}</span>
                <span class="popularity">{topsongs[2][1]}</span>
            </div>
            <div class="song">
                <span class="metric_label">{topsongs[3][0]}</span>
                <span class="popularity">{topsongs[3][1]}</span>
            </div>
            <div class="song">
                <span class="metric_label">{topsongs[4][0]}</span>
                <span class="popularity">{topsongs[4][1]}</span>
            </div>
          <h6>◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍ - ◍</h6 >
          <div class="metrics">
            <div class="metric"><strong>Popularity: </strong>{" - ".join(str(round(x)) for x in popularity_distribution)}</div>
            <div class="metric"><strong>Energy: </strong>{" - ".join(str(round(x,2)) for x in energy_distribution)}</div>
            <div class="metric"><strong>Danceability: </strong>{" - ".join(str(round(x,2)) for x in dance_distribution)}</div>
            <div class="metric"><strong>Emotion: </strong>{" - ".join(str(round(x,2)) for x in emotion_distribution)}</div>
          </div>
        </div>
    </div>
</body>
""", unsafe_allow_html=True)






st.divider()
#   3 metric cards b4
# column layout
    # col1, col2 = st.columns([1,1])  # Adjust the column widths as needed
    # selection = result.loc[result['artist_name'] == selected_name]
    # col1.metric('popularity', selection['popularity'][0])
    # col2.metric('followers', f"{int(selection['followers'][0]):,}")
    # st.metric('genres', \
    #     ", ".join(genre for genre in selection['genres'][0].split('-')),\
    #         )
    # style_metric_cards(background_color="#000000",
    #     border_size_px = 0,
    #     border_color= "#9AD8E1",
    #     border_radius_px = 0,
    #     border_left_color = "#9AD8E1",
    #     box_shadow= False)
#
###########################################
###               ALBUM DATA            ###
###########################################
#


# get all album data for artist
album_result = queries._get_albums(selected_artist_uri)

# reordering columns for visualization
album_result = album_result[['images', 'album_uri', 'artist_uris', 'artist_names', 'album_name', 'release_date', 'total_tracks']]



st.dataframe(album_result.drop(['album_uri', 'artist_uris', 'artist_names'], axis=1),
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




