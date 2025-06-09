from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Profiles
from app import db
from sqlalchemy.orm import selectinload
from app.utils.check_file_extension import check_file_extension
import os
from werkzeug.utils import secure_filename


member_profile_bp = Blueprint('member_profile_bp', __name__)


@member_profile_bp.route('/member_profile', methods=['GET'])
@jwt_required()
def member_profile():
    '''
    retrieves a logged in users profile
    '''
    try:
        user_id = int(get_jwt_identity())

        user = Users.query.options(selectinload(Users.profile)).filter_by(id=user_id).first()

        if not user or not user.profile:
            return jsonify({'error': 'User profile not found!'}), 404

        profile = {
            'email': user.email,
            'username': user.username,
            'phone_number': user.phone_number,
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name,
            'profile_picture': user.profile.profile_picture
            }
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

@member_profile_bp.route('/update_member_profile', methods=['PATCH'])
@jwt_required()
def update_member_profile_picture():
    '''
    updates the members profile picture
    '''
    file = request.files.get('image')

    if not file:
        return jsonify({'error': 'Please select one image!'}), 400

    try:
        user_id = int(get_jwt_identity())

        user = Users.query.options(selectinload(Users.profile)).filter_by(id=user_id).first()

        if not user or not user.profile:
            return jsonify({'error': 'User profile not found!'}), 404

        if check_file_extension(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            user.profile.profile_picture = filename
            db.session.commit()
            return jsonify({'success': 'Profile picture updated successfully'}), 200
        else:
            return jsonify({'error': 'Invalid file type!'}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

