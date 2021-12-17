from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# -------------------------------------------------------------------------------
# User: a user lol
# Current Columns:
#   - Username
#   - Email
#   - Hashed Password
#
# Relationships:
#   - One user has many playlists
#   - One user has many user-track plays
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    user_playlists = db.relationship("Playlist", back_populates="playlist_user")
    user_utps = db.relationship("UserTrackPlays", back_populates="utp_user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# Medium: referring to the anime or video game series of the soundtrack
# - each medium will have a number of albums
# - any extra columns?
# Current Columns:
#   - Title
#   - Image
#   - Info Link
#   - Description
#
# Relationships:
#   One medium has many albums
#   One medium has many tracks
class Medium(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    media_image = db.Column(db.String(1000))
    info_link = db.Column(db.String(1000))
    description = db.Column(db.String(1000))

    medium_albums = db.relationship("Album", back_populates="album_medium")
    medium_tracks = db.relationship("Track", back_populates="track_medium")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'mediaImage': self.media_image,
            'infoLink': self.info_link,
            'description': self.description
        }

# --------------------------------------------------------------------------------
# Artist: composer or writer of a album or track
# Current Columns:
#   - Name
#   - Artist Image
#   - Bio
#
# Relationships:
#   - One artist has many albums
#   - One artist has many tracks
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    artist_image = db.Column(db.String(1000))
    bio = db.Column(db.String(1000))

    artist_albums = db.relationship("Album", back_populates="album_artist")
    artist_tracks = db.relationship("Track", back_populates="track_artist")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'artistImage': self.artist_image,
            'bio': self.bio
        }

# --------------------------------------------------------------------------------
# Album: a collection of tracks, each falling under a medium
# Current Columns
#   - Title
#   - Album Image
#   - Artist
#   - Medium Id
#
# Relationships:
#   - Many albums belong to one medium
#   - Many albums belong to one artist
#   - One album has many tracks
class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    album_image = db.Column(db.String(1000))
    artist = db.Column(db.String)
    medium_id = db.Column(db.Integer, db.ForeignKey("media.id"), nullable=False)

    album_medium = db.relationship("Medium", back_populates="medium_albums")
    album_artist = db.relationship("Artist", back_populates="artist_albums")
    album_tracks = db.relationship("Track", back_populates="track_album")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'albumImage': self.album_image,
            'artist': self.artist,
            'mediumId': self.medium_id,
        }

# ---------------------------------------------------------------------------------------
# Track: a song, each belonging to an album
# Current Columns:
#   - Title
#   - Track Image
#   - Track File
#   - Plays (numbers of times played - play defined as a song clicked to be played, not necessarily finished)
#   - Album ID, the album that the track belongs to
#   - Medium ID, the medium that the track belongs to
#
# Relationships:
#   - Many tracks belong to one medium
#   - Many tracks belong to one artist
#   - Many tracks belong to one album
#   - One track has many playlist links
#   - One track has many user-track plays
class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    track_image = db.Column(db.String(1000))
    track_file = db.Column(db.String(1000))
    plays = db.Column(db.Integer)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    medium_id = db.Column(db.Integer, db.ForeignKey("media.id"), nullable=False)

    track_medium = db.relationship("Medium", back_populates="medium_tracks")
    track_artist = db.relationship("Artist", back_populates="artist_tracks")
    track_album = db.relationship("Album", back_populates="album_tracks")
    track_plls = db.relationship("PlaylistLink", back_populates="pll_track")
    track_utps = db.relationship("UserTrackPlays", back_populates="utp_track")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'trackImage': self.track_image,
            'trackFile': self.track_file,
            'albumId': self.album_id,
            'mediumId': self.medium_id,
        }

# ----------------------------------------------------------------------------
# Playlist: a custom list of tracks that users may create
# Current Columns:
#   - Title
#   - User ID
#
# Relationships:
#   - Many playlists belong to one user
#   - One playlist has many playlist links
class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    playlist_user = db.relationship("User", back_populates="user_playlists")
    playlist_plls = db.relationship("PlaylistLink", back_populates="pll_playlist")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'userId': self.user_id,
        }


# ----------------------------------------------------------------------------------
# Playlist Link: a link that connects a playlist and song together, and also contains other relevant info
# Current Columns:
#   - Track ID (track that the link connects to)
#   - Playlist ID (playlist that the link connects to)
#   - Time Added - date of time added, so that users can sort their playlist tracks by date added
#
# Relationships:
#   - Many playlist links belong to one playlist
#   - Many playlist links belong to one track
class PlaylistLink(db.Model):
    __tablename__ = 'playlistlinks'

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)
    time_added = db.Column(db.DateTime(timezone=False))

    pll_playlist = db.relationship("Playlist", back_populates="playlist_plls")
    pll_track = db.relationship("Track", back_populates="track_plls")


# ------------------------------------------------------------
# User-Track Play: a pseudo-join model that tracks the number of times a user has played a track
# Current Columns:
#   - Track ID (track that this join connects to)
#   - User ID (user that this join connects to)
#   - Count: the amounf of times that the specific user has played the specific track
#
# Relationships:
#   - One user-track play belongs to many tracks
#   - One user-track play belongs to many users
class UserTrackPlays(db.Model):
    __tablename__ = 'usertrackplays'

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    count = db.Column(db.Integer)

    utp_track = db.relationship("Track", back_populates="track_utps")
    utp_user = db.relationship("User", back_populates="user_utps")
