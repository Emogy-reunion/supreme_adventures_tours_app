from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_required
from app.models import Users, Profiles
from sqlalchemy.orm import selectinload


member_profile_bp = Blueprint('member_profile_bp', __name__)


@member_profile_bp.route('/member_profile', methods=['GET'])
@jwt_required()
def member_profile():
    '''
    retrieves a logged in users profile
    '''
    try:
        user_id = int(get_jwt_identity)

        user = Users.query.options(selectinload(Users.profile)).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': 'User profile not found!'}), 404

        profile = [{
            'email': user.email,
            'username': user.username,
            'phone_number': user.phone_number,
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name,
            'profile_picture': user.profile.profile_picture
            })
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
