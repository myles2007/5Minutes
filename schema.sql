drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username string not null,
  email string not null,
  pw_hash string not null
);

drop table if exists follower;
create table follower (
  who_id integer,
  whom_id integer
);

drop table if exists message;
create table message (
  message_id integer primary key autoincrement,
  author_id integer not null,
  text string not null,
  pub_date datetime,
  sticky integer default 0
);

drop table if exists daily_songs;
create table daily_songs (
    song_id integer primary key autoincrement,
    song_date datetime not null,
    track_uri string not null,
    artist_uri string not null,
    album_uri string not null,
    track_name string not null,
    artist_name string not null,
    album_name string not null
);
