# HipHop-Analysis-Project
refactor and expansion of Spotify Pipeline. Extraction from Genius and Spotify APIs.

--- supabase doesn't have support for performing aggregates in their queries, so had to mess around a little bit to perform the joins i wanted. 

Broad Overview of Goals:


extraction:
- pull in artist; album; song data
- persist in supabase DB

analysis:
- (temp: download db as csv to ask AI about visuals in streamlit + python syntax)
- connect graphs and streamlit web app to supabase db

automation:
- lambda functions for this process while keeping streamlit site up
