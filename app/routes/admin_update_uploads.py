from flask import Blueprint, jsonify, request
from app.utils.role import role_required
from app.utils.discount import calculate_final_price
from flask_jwt_extended import jwt_required
from app.models import Tours, TourImages


admin_edit_bp = Blueprint('admin_edit_bp', __name__)

@admin_edit_bp.route('/update_tour/<int:tour_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@role_required('admin')
def update_tour(tour_id):
    '''
    allows the admin to edit a specific tour
    the admin can update the entire tour or just parts of it
    '''
    form = UpdateTourForm(request.form)

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data
    start_location = form.start_location.data
    destination = form.destination.data
    description = form.description.data
    start_date = form.start_date.data
    end_date = form.end_date.data
    days = form.days.data
    nights = form.nights.data
    original_price = form.original_price.data
    discount_percent = form.discount_percent.data
    status = form.status.data
    included = form.included.data
    excluded = form.excluded.data

    try:
        tour = Tours.query.filter_by(id=product_id).first()

        if not tour:
            return jsonify({'error': 'Tour not found'}), 404

        if name:
            tour.name = name

        if start_location:
            tour.start_location = start_location

        if destination:
            tour.destination = destination

        if start_date:
            tour.start_date = start_date

        if end_date:
            tour.end_date = end_date

        if days:
            tour.days = days

        if nights:
            tour.nights = nights

        if original_price:
            tour.original_price = original_price
            tour.final_price = original_price

        if discount_percent:
            tour.discount_percent = discount_percent
            tour.final_price = calculate_final_price(original_price=original_price, discount_percent=discount_percent)

        if status:
            tour.status = status

        if included:
            tour.included = included

        if excluded:
            tour.excluded = excluded
        db.session.commit()
        return jsonify({'success': 'Tour updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500






