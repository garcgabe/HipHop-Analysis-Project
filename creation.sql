-- create artists table
CREATE TABLE artists(
    artist_uri varchar(255) primary key,
    artist_name varchar(255) not null,
    popularity integer,
    followers integer,
    genres varchar(255),
    images varchar(500)
);

-- create albums table
CREATE TABLE albums(
    album_uri varchar(255) primary key,
    album_name varchar(255) not null,
    type varchar(255) not null,
    release_date date,
    total_tracks integer,
    images varchar(500)
);

-- create album-artists relations table
CREATE TABLE album_artists(
    album_uri varchar(255) not null,
    artist_uri varchar(255) not null,
    album_name varchar(255) not null,
    artist_name varchar(255) not null,
    PRIMARY KEY (album_uri, artist_uri),
    FOREIGN KEY (album_uri) REFERENCES albums (album_uri) ON DELETE CASCADE,
    FOREIGN KEY (artist_uri) REFERENCES artists (artist_uri) ON DELETE CASCADE
);

-- create songs table
CREATE TABLE songs(
    song_uri varchar(255) primary key,
    song_name varchar(255) not null,
    album_uri varchar(255) not null,
    explicit boolean,
    preview_url varchar(500),
    FOREIGN KEY (album_uri) REFERENCES albums (album_uri) ON DELETE CASCADE
);

-- create song metrics table
CREATE TABLE metrics(
    song_uri varchar(255) primary key,
    song_name varchar(255) not null,
    duration int not null,
    popularity int,
    danceability decimal(4,3),
    energy decimal(4,3),
    loudness decimal(5,3),
    valence decimal(4,3),
    tempo decimal(5,1),
    instrumentalness decimal(4,4),
    speechiness decimal(4,3),
    album_uri varchar(255) not null ,
    FOREIGN KEY (song_uri) REFERENCES songs (song_uri) ON DELETE CASCADE,
    FOREIGN KEY (album_uri) REFERENCES albums (album_uri) ON DELETE CASCADE
);
