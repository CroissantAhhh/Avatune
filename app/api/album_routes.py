from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import db, User, Album, Artist

album_routes = Blueprint('albums', __name__)

@album_routes.route('/<int:album_id>')
def album_by_id(album_id):
    album = Album.query.get(album_id)
    return { "albums": album.to_dict() }

@album_routes.route('/byHash/<album_hash>')
def album_by_hash(album_hash):
    album = Album.query.filter(Album.hashed_id == album_hash).one()
    return { "albums": [ album.to_dict() ] }

@album_routes.route('/latest')
def latest_album():
    all_albums = Album.query.all()
    return { "album": all_albums[-1].to_dict() }

@album_routes.route('/byUser/<int:user_id>')
@login_required
def albums_by_user(user_id):
    user = User.query.get(user_id)
    user_liked_albums = user.user_albums
    return { "albums": [album.to_dict() for album in user_liked_albums] }

@album_routes.route('/byMedia/<int:medium_id>')
@login_required
def albums_by_media(medium_id):
    return { "albums": [album.to_dict() for album in Album.query.filter(Album.medium_id == medium_id).all()] }

@album_routes.route('/byArtist/<int:artist_id>')
@login_required
def albums_by_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return { "albums": [album.to_dict() for album in artist.artist_albums] }

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

def find_searched_albums(album_search):
    search_terms = album_search.split(" ")
    album_matches = []
    for i in range(len(search_terms), 0, -1):
        album_found = Album.query.filter(terms_matched(Album.title, album_search) == i)
        for found_album in album_found:
            album_matches.append(found_album.to_dict())
    return album_matches

@album_routes.route('/search/<album_search>')
def albums_search(album_search):
    return { "albums": find_searched_albums(album_search)[-5:] }

@album_routes.route('/fullSearch/<album_search>')
def albums_full_search(album_search):
    return { "albums": find_searched_albums(album_search) }

@album_routes.route('/like', methods=['POST'])
def like_album():
    data = request.json
    user = User.query.get(data["userId"])
    album = Album.query.get(data["albumId"])
    user.user_albums.append(album)
    album.album_users.append(user)
    db.session.commit()
    return { "albums": album }
