from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User, Artist

artist_routes = Blueprint('artists', __name__)

@artist_routes.route('/<int:artist_id>')
def artist_by_id(artist_id):
    artist = Artist.query.get(artist_id)
    return { "artists": artist.to_dict() }


@artist_routes.route('/byUser/<int:user_id>')
@login_required
def artists_by_user(id):
    user = User.query.get(id)
    user_liked_artists = user.user_artists
    return { "artists": [artist.to_dict() for artist in user_liked_artists] }

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

# Finds all artists that satisfy the search query, sorted from most fitting to least fitting
def find_searched_artists(artist_search):
    search_terms = artist_search.split(" ")
    artist_matches = []
    for i in range(len(search_terms), 0, -1):
        artist_found = Artist.query.filter(terms_matched(Artist.name, artist_search) == i)
        for found_artist in artist_found:
            artist_matches.append(found_artist.to_dict())
    return artist_matches

@artist_routes.route('/search/<artist_search>')
def artists_search(artist_search):
    return { "artists": find_searched_artists(artist_search)[-5:] }

@artist_routes.route('/fullSearch/<artist_search>')
def artists_full_search(artist_search):
    return { "artists": find_searched_artists(artist_search) }
