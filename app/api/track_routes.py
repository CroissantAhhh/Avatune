from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import db, User, Track, UserTrackPlays

track_routes = Blueprint('tracks', __name__)

@track_routes.route('/<int:track_id>')
def track_by_id(track_id):
    track = Track.query.get(track_id)
    return { "tracks": track.to_dict() }


@track_routes.route('/byUser/<int:user_id>')
@login_required
def tracks_by_user(id):
    user = User.query.get(id)
    user_liked_tracks = user.user_tracks
    return { "tracks": [track.to_dict() for track in user_liked_tracks] }

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

@track_routes.route('/mostPlayed/<int:user_id>')
def user_most_played(user_id):
    user_track_plays = UserTrackPlays.query.filter(UserTrackPlays.user_id == user_id).all()
    user_track_plays.sort(reverse=True, key=lambda x: x.count)
    return { "tracks": [track.to_dict() for track in user_track_plays[0:10]] }

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
    db.session.commit()
