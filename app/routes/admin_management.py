from flask import Blueprint, jsonify
from app.models import Users, Profiles
from sqlalchemy.orm import selectinload
from flask_jwt_extended import jwt_required
from app.utils.role import role_required



admin_manage_bp = Blueprint('admin_manage_bp', __name__)


@admin_manage_bp.route('/view_admins', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_admins():
    '''
    retrieves all admins from the database
    '''
    try:
        admins = Users.query.options(selectinload(Users.profile)).filter_by(role='admin').all()

        if not admins:
            return jsonify({'error': 'No admins found in the system!'}), 404

        admin_details = [{
            'admin_id': admin.id,
            'first_name': admin.profile.first_name,
            'last_name': admin.profile.last_name,
            'profile_picture': admin.profile.profile_picture,
            } for admin in admins]
        return jsonify(admin_details), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500

