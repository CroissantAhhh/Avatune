from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import db, User, Artist, Track, Playlist, PlaylistLink, UserTrackPlays
import datetime as dt

track_routes = Blueprint('tracks', __name__)

@track_routes.route('/<int:track_id>')
def track_by_id(track_id):
    track = Track.query.get(track_id)
    return { "tracks": track.to_dict() }


@track_routes.route('/byUser/<int:user_id>')
@login_required
def tracks_by_user(user_id):
    user = User.query.get(user_id)
    user_liked_tracks = user.user_tracks
    return { "tracks": [track.to_dict() for track in user_liked_tracks] }

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

# Finds all tracks that satisfy the search query, sorted from most fitting to least fitting
def find_searched_tracks(track_search):
    search_terms = track_search.split(" ")
    track_matches = []
    for i in range(len(search_terms), 0, -1):
        track_found = Track.query.filter(terms_matched(Track.title, track_search) == i)
        for found_track in track_found:
            track_matches.append(found_track.to_dict())
    return track_matches

@track_routes.route('/search/<track_search>')
def tracks_search(track_search):
    return { "tracks": find_searched_tracks(track_search)[-5:] }

@track_routes.route('/fullSearch/<track_search>')
def tracks_full_search(track_search):
    return { "tracks": find_searched_tracks(track_search) }

@track_routes.route('/userMost/<int:user_id>')
def user_most_played(user_id):
    user_track_plays = UserTrackPlays.query.filter(UserTrackPlays.user_id == user_id).all()
    if len(user_track_plays) <= 5:
        return { "tracks": [Track.query.get(track.track_id).to_dict() for track in user_track_plays] }
    else:
        user_track_plays.sort(reverse=True, key=lambda x: x.count)
        return { "tracks": [Track.query.get(track.track_id).to_dict() for track in user_track_plays[0:5]] }

@track_routes.route('/mediumMost/<int:medium_id>')
def medium_most_played(medium_id):
    medium_most = Track.query.filter(Track.medium_id == medium_id).all()
    medium_most.sort(reverse=True, key=lambda x: x.plays)
    return { "tracks": [track.to_dict() for track in medium_most[0:10]] }

@track_routes.route('/artistMost/<int:artist_id>')
def artist_most_played(artist_id):
    artist_most = Track.query.filter(Artist.query.get(artist_id) in Track.track_artists).all()
    artist_most.sort(reverse=True, key=lambda x: x.plays)
    return { "tracks": [track.to_dict() for track in artist_most[0:10]] }

@track_routes.route('/playTrack/<int:user_id>/<int:track_id>', methods=['POST'])
def play_track(user_id, track_id):
    user_track_query = UserTrackPlays.query.filter(UserTrackPlays.user_id == user_id and UserTrackPlays.track_id == track_id)
    if user_track_query.count() == 0:
        new_utp = UserTrackPlays(
            track_id = track_id,
            user_id = user_id,
            count = 1,
        )
        db.session.add(new_utp)
    else:
        found_utp = user_track_query.one()
        found_utp.count += 1

    track = Track.query.get(track_id)
    track.plays += 1

    user = User.query.get(user_id)
    track_id_string = str(track_id)
    user_recently_played = user.recently_played
    if user_recently_played == "":
        user.recently_played = track_id_string
    else:
        recent_tracks = user_recently_played.split("-")
        if track_id_string in recent_tracks:
            recent_tracks.remove(track_id_string)
        recent_tracks.insert(0, track_id_string)
        if len(recent_tracks) > 5:
            recent_tracks.pop(5)
    db.session.commit()

@track_routes.route('/addPlaylist/<int:playlist_id>/<int:track_id>', methods=['POST'])
def add_track_playlist(playlist_id, track_id):
    new_pll = PlaylistLink(
        track_id = track_id,
        playlist_id = playlist_id,
        time_added = dt.datetime.now()
    )
    db.session.add(new_pll)
    db.session.commit()
    plls = PlaylistLink.query.filter(PlaylistLink.playlist_id == playlist_id).all()
    return { "tracks": [Track.query.get(pll.track_id).to_dict() for pll in plls]}

@track_routes.route('/removePlaylist/<int:playlist_id>/<int:track_id>', methods=['DELETE'])
def remove_track_playlist(playlist_id, track_id):
    pll = PlaylistLink.query.filter(PlaylistLink.playlist_id == playlist_id and PlaylistLink.track_id == track_id).one()
    db.session.delete(pll)
    db.session.commit()
    plls = PlaylistLink.query.filter(PlaylistLink.playlist_id == playlist_id).all()
    return { "tracks": [Track.query.get(pll.track_id).to_dict() for pll in plls]}
