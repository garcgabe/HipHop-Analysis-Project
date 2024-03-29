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

topsongs = queries._get_top_songs(selected_name, 5)
popularity_distribution = queries._get_distribution(selected_name, 'popularity')
dance_distribution = queries._get_distribution(selected_name, 'danceability')
emotion_distribution = queries._get_distribution(selected_name,'valence')
energy_distribution = queries._get_distribution(selected_name, 'energy') 

all_songs_statistics = queries._get_all_song_statistics(selected_artist_uri)

#card = pareto_card.generate(selected_name, selected_artist_genres, selected_artist_image)
# st.markdown(card[0], unsafe_allow_html=True)
# st.markdown(card[1], unsafe_allow_html=True)
CSS_STYLES = st.markdown("""
    <style>
    .container { text-align: center; justify-content: center; margin-bottom: 5px; padding-top: 10px; }
    .img_container { text-align: center; justify-content: center; margin-bottom: 5px; padding-bottom: 10px;}

    .metric_holder { background-color: #000000; padding-top: 10px;
                border: 2px solid #887b56;
                padding: 2%;
                border-radius: 2px;
                border-left: 0.5rem solid #887b56;}
    .metric { padding-top: 3px; display: flex; justify-content: space-between; padding-left: 20px; padding-right: 20px; }
    .metric_label { text-align: left; font-size: 20px; font-weight: bold; color: #887b56; padding-left: 20px;}
    .metric_value { text-align: right; padding-right: 20px; color: #f1f1f1; font-size: 16px}
    .song { display: flex; justify-content: space-between; padding-top: 5px}
    .title {text-align: left; }
    .popularity { text-align: right; padding-right: 20px; }
    .metrics { text-align: bottom; }
    .metric_title { display: flex; justify-content: space-between;font-size: 16px; font-weight: bold; color: #887b56; 
            border-bottom: 2px solid #f1f1f1; padding-bottom: 3px; transition: border-width 0.3s;
            padding-left: 20px; padding-right: 20px;}
    .metric_title:hover {border-bottom-width: 8px;}
    .divider {border-bottom: 4px solid #887b56; padding-bottom: 3px; transition: border-width 0.3s;
            padding_top: 20px; }
    .divider:hover {border-bottom-width: 12px;}

    h6 { color: #887b56; font-size: 20px; font-weight: bold; padding-top: 5px; padding-bottom: 5px; }

    </style>
""", unsafe_allow_html=True)


home_tab, artist_tab, albums_tab, songs_tab = st.tabs([":white[home]", ":red[artist]", ":red[albums]", ":red[songs]"])

with home_tab:
    ### ARTIST pic
    st.markdown(f"""
        <body>
        <div class="img_container">
            <img src={selected_artist_image} height="300"></img>
        </div>
    </body>
    """, unsafe_allow_html=True)

    albums = queries._get_albums(selected_artist_uri)

    # reordering columns for visualization
    album_result = albums[['images', 'album_uri', 'artist_uris', 'artist_names', 'album_name', 'release_date', 'total_tracks']]
    st.dataframe(album_result.drop(['album_uri', 'artist_uris', 'artist_names'], axis=1),
        column_config={
            "images": st.column_config.ImageColumn("album cover"),
            "album_name": st.column_config.TextColumn("album"),
            "release_date": st.column_config.TextColumn("release date"),
            "total_tracks": st.column_config.TextColumn("album length"),
        }, use_container_width=True, hide_index=True)

with artist_tab:
    ### ARTIST_INFO
    st.markdown(f"""
    <body>
        <div class="img_container">
            <img src={selected_artist_image} width="200" height="200"></img>
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
            <div class="divider"></div>
    </body>
    """, unsafe_allow_html=True)
    ### METRICS_TABLE 
    st.markdown(f"""
    <body>
        <div class="container">
            <div class="metric_holder">
            <div class="metric_title"><strong>Song </strong>Popularity</div>
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
                <div class="metric_title"><strong>Metric </strong>Min | Avg | Max</div>
                <div class="metric"><strong>Popularity</strong>{" - - - ".join(str(round(x)) for x in popularity_distribution)}</div>
                <div class="metric"><strong>Energy</strong>{" - ".join(str(round(x,2)) for x in energy_distribution)}</div>
                <div class="metric"><strong>Danceability</strong>{" - ".join(str(round(x,2)) for x in dance_distribution)}</div>
                <div class="metric"><strong>Emotion</strong>{" - ".join(str(round(x,2)) for x in emotion_distribution)}</div>
            </div>
            </div>
        </div>
    </body>
    """, unsafe_allow_html=True)

with albums_tab:
    ### ALBUMS
    album_averages = all_songs_statistics.groupby("album_name")[["popularity", "danceability", "energy", "valence"]].mean().round(2)
    album_averages["album name"] = album_averages.index
    st.dataframe(album_averages[["album name", "popularity", "danceability", "energy", "valence"]], use_container_width=True, hide_index=True)

with songs_tab:
    albums = queries._get_albums(selected_artist_uri)
    selected_album = st.selectbox("select an album to view", options=albums["album_name"])
    st.dataframe(all_songs_statistics[all_songs_statistics["album_name"] == selected_album], use_container_width=True, hide_index=True)

#
#
# 
#
#




