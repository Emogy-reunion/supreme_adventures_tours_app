from flask import Blueprint, jsonify
from app.models import Tours, TourImages
from app import db
from flask_jwt_extended import jwt_required
from app.utils.role import role_required
import os
from sqlalchemy.orm import selectinload


admin_delete_bp = Blueprint('admin_delete_bp', __name__)


@admin_delete_bp.route('/delete_tour/<int:tour_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_tour(tour_id):
    '''
    deletes a specific tour
    '''
    try:
        tour = Tours.query.options(selectinload(Tours.images)).filter_by(id=tour_id).first()
        if not tour:
            return jsonify({'error': 'Tour not found!'}), 404

        for image in tour.images:
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            
            if os.path.exists(upload_path):
                os.remove(upload_path)
        db.session.delete(tour)
        db.session.commit()
        return jsonify({'success': 'Tour successfully deleted!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500


