from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

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


class Medium(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    media_image = db.Column(db.String(1000))
    description = db.Column(db.String(1000))

    medium_albums = db.relationship("Album", back_populates="album_medium")
    medium_tracks = db.relationship("Track", back_populates="track_medium")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'mediaImage': self.media_image,
            'description': self.description
        }


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    album_image = db.Column(db.String(1000))
    artist = db.Column(db.String)
    medium_id = db.Column(db.Integer, db.ForeignKey("media.id"), nullable=False)

    album_medium = db.relationship("Medium", back_populates="medium_albums")
    album_tracks = db.relationship("Track", back_populates="track_album")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'albumImage': self.album_image,
            'artist': self.artist,
            'mediumId': self.medium_id,
        }

class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    track_image = db.Column(db.String(1000))
    track_file = db.Column(db.String(1000))
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    medium_id = db.Column(db.Integer, db.ForeignKey("media.id"), nullable=False)

    track_album = db.relationship("Album", back_populates="album_tracks")
    track_medium = db.relationship("Medium", back_populates="medium_tracks")
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


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    playlist_plls = db.relationship("PlaylistLink", back_populates="pll_playlist")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'userId': self.user_id,
        }


class PlaylistLink(db.Model):
    __tablename__ = 'playlistlinks'

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)
    time_added = db.Column(db.DateTime(timezone=False))

    pll_playlist = db.relationship("Playlist", back_populates="playlist_plls")
    pll_track = db.relationship("Track", back_populates="track_plls")

class UserTrackPlays(db.Model):
    __tablename__ = 'usertrackplays'

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    count = db.Column(db.Integer)

    utp_track = db.relationship("Track", back_populates="track_utps")
    utp_user = db.relationship("User", back_populates="user_utps")
