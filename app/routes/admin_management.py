from flask import Blueprint, jsonify, current_app, request
from app.models import Users, Profiles
from sqlalchemy.orm import selectinload
from flask_jwt_extended import jwt_required
from app.utils.role import role_required
from app.forms import EmailForm
from app import db
from app.background.admin_promotion_email import send_admin_promotion_email
from app.background.revoke_admin_email import send_admin_revoke_email



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
        return jsonify({'admins': admin_details}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@admin_manage_bp.route('/promote_user', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def promote_user():
    form = EmailForm(data=request.get_json())

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    email = form.email.data.strip().lower()
    try:
        user = Users.query.filter_by(email=email).first()

        if user and user.role == 'member':
            user.role = 'admin'
            db.session.commit()
            send_admin_promotion_email.delay(email)
            return jsonify({'success': 'User promoted to admin successfully!'}), 200
        else:
            return jsonify({'error': "User doesn't exist or already has admin privileges"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@admin_manage_bp.route('/revoke_admin_privileges', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def revoke_admin_privileges():
     try:
         user_id = request.json.get('admin_id')

         user = db.session.get(Users, user_id)

         if not user or user.role != 'admin' or user.email == current_app.config['DEFAULT_MAIL_SENDER']:
             return jsonify({'error': "User not found or doesn't have admin privileges!"}), 404

         user.role = 'member';
         db.session.commit()
         send_revoke_admin_email.delay(user.email)
         return jsonify({'success': "User's admin privileges revoked!"}), 200
     except Exception as e:
         db.session.rollback()
         return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500
