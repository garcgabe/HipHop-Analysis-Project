# HipHop-Analysis-Project
refactor and expansion of Spotify Pipeline. Extraction from Genius and Spotify APIs.

--- supabase doesn't have support for performing aggregates in their queries, so had to mess around a little bit to perform the joins i wanted. 

-- todo:
--  - add timestamps for all tables

Broad Overview of Goals:

db redesign:
fact: (song_uri, )
albums: (PK album_id)
album_artist_relations: (PK )


extraction:
- pull in artist; album; song data
- persist in supabase DB

analysis:
- (temp: download db as csv to ask AI about visuals in streamlit + python syntax)
- connect graphs and streamlit web app to supabase db

automation:
- lambda functions for this process while keeping streamlit site up


ROLE OF SUPABASE:
- initially, all data is pushed into supabase. this is done since it's a free tier cloud DB and i'd like to have this up
- supabase's db abstraction is limiting, especially for analytics querying (aggregates limited, annoying) and I have to write weirdly translated code instead of simple SQL
- due to this - going to have to set up direct connection in datagrip w the supabase db underlying. no abstractions if i can get away with it


## Database Design

![Design](https://github.com/garcgabe/HipHop-Analysis-Project/blob/main/hh_db_design.png "Storage of Albums, Artists, Songs, and Relationships")
