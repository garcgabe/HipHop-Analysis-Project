# HipHop-Analysis-Project
refactor and expansion of Spotify Pipeline. Extraction from Genius and Spotify APIs.

implementation notes:
- initially used spotipy wrapper for easy auth - later tried using requests library. bearer auth is needed with access token, and tokens expires after 1 hour. for ease of development, spotipy is easier since i already have the wrapper. could build in functionality to request new token after an hour, but instead just going ahead. 
- fetching song data. first, have to get songs from albums using Get Album Tracks, then get song data from Get Track and Get Track Audio Features


notes: 
- The Black Album (Jay Z) and Well Done (Action Bronson) have duplicates on their album names, but not the URI. should be looked into
query to replicate: 
        select * from albums where album_name in (select album_name from albums
        group by 1
        having count(album_name) = 2)

- there are many song duplicates
---- they may be same song name, diff artist, same song name, same artist, diff album, and these have different song_uris, so may have to create some logic that aggregates the songs if they're on different albums.

with multiple_songs as (
	select song_name--, count(album_uri) as occurrences 
	from songs
	group by song_name
	having count(album_uri) > 1
	)
select song_name, album_uri from songs 
where song_name in (select song_name from multiple_songs) 
order by song_name

