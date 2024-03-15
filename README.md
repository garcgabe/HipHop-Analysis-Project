# HipHop-Analysis-Project
refactor and expansion of Spotify Pipeline. Extraction from Genius and Spotify APIs.

implementation notes:
- initially used spotipy wrapper for easy auth - later tried using requests library. bearer auth is needed with access token, and tokens expires after 1 hour. for ease of development, spotipy is easier since i already have the wrapper. could build in functionality to request new token after an hour, but instead just going ahead. 
- fetching song data. first, have to get songs from albums using Get Album Tracks, then get song data from Get Track and Get Track Audio Features





--- supabase doesn't have support for performing aggregates in their queries, so had to mess around a little bit to perform the joins i wanted. 

