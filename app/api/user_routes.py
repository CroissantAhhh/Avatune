from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User, Follow

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def one_user(id):
    user = User.query.get(id)
    return {'users': user.to_dict() }

@user_routes.route('/byHash/<user_hash>')
@login_required
def one_user_by_hash(user_hash):
    user = User.query.filter(User.hashed_id == user_hash).one()
    return {'users': [ user.to_dict() ] }

@user_routes.route('/followers/<int:id>')
@login_required
def user_followers(id):
    followers = Follow.query.filter(Follow.followed_id == id).all()
    return {'users': [User.query.get(follower.follower_id).to_dict() for follower in followers] }

@user_routes.route('/following/<int:id>')
@login_required
def user_following(id):
    following = Follow.query.filter(Follow.follower_id == id).all()
    return {'users': [User.query.get(followed.followed_id).to_dict() for followed in following] }
