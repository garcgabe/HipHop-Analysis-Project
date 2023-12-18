-- create artists table
CREATE TABLE artists(
    artist_uri varchar(256) primary key,
    artist_name varchar(256),
    spotify_name varchar(256),
    popularity integer,
    followers integer,
    genres varchar(256),
    images varchar(256)
);

-- create albums table
CREATE TABLE albums(
    album_uri varchar(256) primary key,
    album_name varchar(256) not null,
    total_tracks integer,
    release_date date,
    artist_uris varchar(256),
    artist_names varchar(256),
    images varchar(256)
);

-- create songs table
CREATE TABLE songs(
    song_uri varchar(256) primary key,
    song_name varchar(256) not null,
    album_uri varchar(256),
    artist_names varchar(256),
    explicit boolean,
    preview_url varchar(256),
    FOREIGN KEY (album_uri) REFERENCES albums (album_uri) ON DELETE CASCADE
);

-- create song metrics table
CREATE TABLE metrics(
    song_uri varchar(256),
    dance decimal(4,3),
    energy decimal(4,3),
    loudness decimal(5,3),
    valence decimal(4,3),
    tempo decimal(5,1),
    instru decimal(4,4),
    speech decimal(4,3)
   -- FOREIGN KEY (song_uri) REFERENCES songs (song_uri)
);
