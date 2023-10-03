# HipHop-Analysis-Project
refactor and expansion of Spotify Pipeline. Extraction from Genius and Spotify APIs.

notes: 
- The Black Album (Jay Z) and Well Done (Action Bronson) have duplicates on their album names, but not the URI. should be looked into
query to replicate: 
        select * from albums where album_name in (select album_name from albums
        group by 1
        having count(album_name) = 2)

- you can just dump all the songs into SQL for now. if there happen to be duplicates based on explicit/clean,
we can add SQL logic to clean it up. just dump it all there for now and use SQL to filter and slice

- there are many song duplicates
---- they may be same song name, diff artist, same song name, same artist, diff album, and these have different song_uris, so may have to create some logic that aggregates the songs if they're on different albums.

-- idk we'll see