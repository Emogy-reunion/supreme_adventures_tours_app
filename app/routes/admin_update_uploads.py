from flask import Blueprint, jsonify, request
from app.utils.role import role_required
from app.utils.discount import calculate_final_price
from flask_jwt_extended import jwt_required
from app import models, db
from app.models import Tours, TourImages, Products, ProductImages
from app.forms import UpdateTourForm, UpdateMerchandiseForm
from sqlalchemy.orm import selectinload


admin_edit_bp = Blueprint('admin_edit_bp', __name__)


@admin_edit_bp.route('/update_tour/<int:tour_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_tour(tour_id):
    '''
    allows the admin to edit a specific tour
    it updates the entire resource so the put method is used
    '''
    form = UpdateTourForm(data=request.form)

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data.strip().lower()
    start_location = form.start_location.data.strip().lower()
    destination = form.destination.data.strip().lower()
    description = form.description.data.strip()
    start_date = form.start_date.data
    end_date = form.end_date.data
    days = form.days.data
    nights = form.nights.data
    original_price = form.original_price.data
    discount_percent = form.discount_percent.data
    status = form.status.data.strip().lower()
    included = form.included.data
    excluded = form.excluded.data

    try:
        tour = Tours.query.options(selectinload(Tours.images)).filter_by(id=tour_id).first()

        if not tour:
            return jsonify({'error': 'Tour not found'}), 404

        if name and tour.name != name:
            tour.name = name

        if start_location and tour.start_location != start_location:
            tour.start_location = start_location

        if destination and tour.destination != destination:
            tour.destination = destination

        if start_date and tour.start_date != start_date:
            tour.start_date = start_date

        if end_date and tour.end_date != end_date:
            tour.end_date = end_date

        if days and tour.days != days:
            tour.days = days

        if nights and tour.nights != nights:
            tour.nights = nights

        if original_price and tour.original_price != original_price:
            tour.original_price = original_price
            tour.final_price = original_price

        if discount_percent and tour.discount_percent != discount_percent:
            tour.discount_percent = discount_percent
            tour.final_price = calculate_final_price(original_price=tour.original_price, discount_percent=tour.discount_percent)

        if status and tour.status != status:
            tour.status = status

        if included and tour.included != included:
            tour.included = included

        if excluded and tour.excluded != excluded:
            tour.excluded = excluded
        db.session.commit()

        updated_tour = {
                'tour_id': tour.id,
                'name': tour.name.title(),
                'start_location': tour.start_location.title(),
                'destination': tour.destination.title(),
                'description': tour.description,
                'start_date': tour.start_date.strftime("%B %d, %Y, %I:%M %p"),
                'end_date': tour.end_date.strftime("%B %d, %Y, %I:%M %p"),
                'days': tour.days,
                'nights': tour.nights,
                'original_price': tour.original_price,
                'final_price': tour.final_price,
                'discount': tour.discount_percent,
                'status': tour.status.title(),
                'included': tour.included,
                'excluded': tour.excluded,
                'image': tour.images[0].filename if tour.images else None
                }
        return jsonify({
            'updated_tour': updated_tour,
            'success': 'Tour updated successfully!'
            }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@admin_edit_bp.route('/update_merchandise/<int:product_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_merchandise(product_id):
    '''
    updates a specific merchandise
    updates the entire resource
    '''
    form = UpdateMerchandiseForm(data=request.form)

    if not form.validate():
        return jsonify({'error': form.errors}), 400

    name = form.name.data.strip().lower()
    product_type = form.product_type.data.strip().lower()
    orginal_price = form.original_price.data
    discount_rate = form.discount_rate.data
    status = form.status.data.strip().lower()
    size = form.size.data.strip().lower()
    description = form.description.data.strip()

    try:
        product = Products.query.options(selectinload(Products.images)).filter_by(id=product_id).first()

        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        if name and product.name != name:
            product.name = name

        if product_type and product.product_type != product_type:
            product.product_type = product_type

        if original_price and product.original_price != original_price:
            product.original_price = original_price
            final_price = original_price

        if discount_percent and product.discount_percent != discount_percent:
            product.discount_percent = discount_percent
            product.final_price = calculate_final_price(original_price=product.original_price, discount_percent=product.discount_percent)

        if status and product.status != status:
            product.status = status

        if size and product.size != size:
            product.size = size

        if description and product.description != description:
            product.description = description

        db.session.commit()

        updated_product = {
                'product_id': product.id,
                'name': product.name.title(),
                'original_price': product.original_price,
                'discount_rate': product.discount_rate,
                'final_price': product.final_price,
                'status': product.status.capitalize(),
                'size': product.size,
                'status': product.status,
                'image': product.images[0].filename if product.images else None
                }
        return jsonify({
            'updated_product': updated_product,
            'success': 'Tour updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500
