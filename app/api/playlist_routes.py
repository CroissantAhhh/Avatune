from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import db, User, Track, Playlist, PlaylistLink, UserTrackPlays
import string
from random import choice

playlist_routes = Blueprint('playlists', __name__)

@playlist_routes.route('/<int:playlist_id>')
def playlist_by_id(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    return { "playlists": playlist.to_dict() }

@playlist_routes.route('/byHash/<playlist_hash>')
def playlist_by_hash(playlist_hash):
    playlist = Playlist.query.filter(Playlist.hashed_id == playlist_hash).one()
    return { "playlists": [playlist.to_dict()]}

# Calculates the total number of plays for all songs in a playlist, divided by
# the number of songs. This is to calculate how often a user listens to a playlist
def average_track_plays(user_id, playlist_id):
    playlist = Playlist.query.get(playlist_id)
    playlist_links = PlaylistLink.query.filter(PlaylistLink.playlist_id == playlist.id).all()
    play_count = 0
    for pll in playlist_links:
        utp = UserTrackPlays.query.filter(UserTrackPlays.user_id == user_id and UserTrackPlays.track_id == pll.track_id).one()
        play_count += utp.count
    return ( play_count / len(playlist_links) )

@playlist_routes.route('/byUserMost/<int:user_id>')
@login_required
def playlists_by_user_most(user_id):
    user = User.query.get(user_id)
    user_owned_playlists = user.user_playlists
    if len(user_owned_playlists) <= 5:
        return { "playlists": [playlist.to_dict() for playlist in user_owned_playlists] }
    else:
        user_owned_playlists.sort(reverse=True, key=lambda x: average_track_plays(user_id, x.id))
        return { "playlists": [playlist.to_dict() for playlist in user_owned_playlists[0:5]] }

@playlist_routes.route('/byUser/<int:user_id>')
@login_required
def playlists_by_user(user_id):
    user = User.query.get(user_id)
    user_owned_playlists = user.user_playlists
    user_followed_playlists = user.user_followed_playlists
    user_playlists = user_owned_playlists + user_followed_playlists
    return { "playlists": [playlist.to_dict() for playlist in user_playlists] }

# Helper function for the search algorithm
def terms_matched(title, search_term):
    matches = []
    search_terms = search_term.split(" ")
    title_terms = title.split(" ")
    for title_term in title_terms:
        for i in range(len(title_term)):
            letters_only = filter(str.isalpha, title_term[i])
            title_term = "".join(letters_only)

    for st in search_terms:
        for tt in title_terms:
            if st in tt:
                if st not in matches:
                    matches.append(st)

    return len(matches)

# Finds all playlists that satisfy the search query, sorted from most fitting to least fitting
def find_searched_playlists(playlist_search):
    search_terms = playlist_search.split(" ")
    playlist_matches = []
    for i in range(len(search_terms), 0, -1):
        playlist_found = Playlist.query.filter(terms_matched(Playlist.title, playlist_search) == i)
        for found_playlist in playlist_found:
            playlist_matches.append(found_playlist.to_dict())
    return playlist_matches

@playlist_routes.route('/search/<playlist_search>')
def playlists_search(playlist_search):
    return { "playlists": find_searched_playlists(playlist_search)[-5:] }

@playlist_routes.route('/fullSearch/<playlist_search>')
def playlists_full_search(playlist_search):
    return { "playlists": find_searched_playlists(playlist_search) }

def generate_hash_id():
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(20))

@playlist_routes.route('/')
def create_playlist():
    data = request.json
    new_playlist = Playlist(
        hashed_id = generate_hash_id(),
        title = data["title"],
        user_id = data["userId"],
    )
    db.session.add(new_playlist)
    db.session.commit()
    user = User.query.get(data["userId"])
    user_owned_playlists = user.user_playlists
    user_followed_playlists = user.user_followed_playlists
    user_playlists = user_owned_playlists + user_followed_playlists
    return { "playlists": [playlist.to_dict() for playlist in user_playlists] }
