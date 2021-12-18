from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import db, User, Medium

media_routes = Blueprint('media', __name__)

@media_routes.route('/<int:medium_id>')
def medium_by_id(medium_id):
    medium = Medium.query.get(medium_id)
    return { "media": medium.to_dict() }


@media_routes.route('/byUser/<int:user_id>')
@login_required
def medium_by_user(id):
    user = User.query.get(id)
    user_liked_media = user.user_media
    return { "media": [medium.to_dict() for medium in user_liked_media] }

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

def find_searched_media(media_search):
    search_terms = media_search.split(" ")
    media_matches = []
    for i in range(len(search_terms), 0, -1):
        media_found = Medium.query.filter(terms_matched(Medium.title, media_search) == i)
        for found_media in media_found:
            media_matches.append(found_media.to_dict())
    return media_matches

@media_routes.route('/search/<media_search>')
def medium_search(media_search):
    return { "media": find_searched_media(media_search)[-5:] }

@media_routes.route('/fullSearch/<media_search>')
def medium_full_search(media_search):
    return { "media": find_searched_media(media_search) }

@media_routes.route('/follow/<int:user_id>/<int:medium_id>')
def follow_medium(user_id, medium_id):
    user = User.query.get(user_id)
    medium = Medium.query.get(medium_id)
    user.user_media.append(medium)
    medium.media_users.append(user)
    db.session.commit()
    return { "media": [media.to_dict() for media in user.user_media]}
