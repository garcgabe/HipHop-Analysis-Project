-- load into artists
\COPY artists FROM '/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifyArtists' DELIMITER ',' CSV HEADER;

-- load into albums
\COPY albums FROM '/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifyAlbums' DELIMITER ',' CSV HEADER;

-- load into songs
\COPY songs FROM '/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifySongs' DELIMITER ',' CSV HEADER;

-- load into metrics
\COPY metrics FROM '/Users/garcgabe/Desktop/HipHop-Analysis-Project/data/SpotifySongsMetrics' DELIMITER ',' CSV HEADER;
