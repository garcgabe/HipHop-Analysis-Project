# HipHop-Analysis-Project
refactor and expansion of Spotify Pipeline. Extraction from Genius and Spotify APIs.

notes: 
- The Black Album (Jay Z) and Well Done (Action Bronson) have duplicates on their album names, but not the URI. should be looked into
query to replicate: 
        select * from albums where album_name in (select album_name from albums
        group by 1
        having count(album_name) = 2)
