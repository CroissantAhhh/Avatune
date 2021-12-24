import boto3
import botocore
from flask import Blueprint, request
from flask_login import login_required

from app.config import Config
from app.aws_s3 import *
from app.models import db, User, Playlist

file_routes = Blueprint('file', __name__)

@file_routes.route('/user', methods=["POST"])
@login_required
def upload_user_image():
    if "file" not in request.files:
        return "No user_file key in request.files"

    image_file = request.files["file"]
    user_id = request.form.get("userId")
    user = User.query.get(user_id)

    if image_file:
        image_file_url = upload_file_to_s3(image_file, Config.S3_BUCKET)

        user.image = image_file_url

        db.session.commit()
        return { 'user': user.to_dict() }

@file_routes.route('/playlist', methods=["POST"])
@login_required
def upload_playlist_image():
    if "file" not in request.files:
        return "No user_file key in request.files"

    image_file = request.files["file"]
    playlist_id = request.form.get("playlistId")
    playlist = Playlist.query.get(playlist_id)

    if image_file:
        image_file_url = upload_file_to_s3(image_file, Config.S3_BUCKET)

        playlist.image = image_file_url

        db.session.commit()
        return { 'playlist': playlist.to_dict() }
