from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity


book = Blueprint('book', __name__)

@book.route('/book', methods=['POST'])
@jwt_required()
def book():
    '''
    allows users to book tours
    '''
    tour_id = request.json.get('tour_id')
    user_id = get_jwt_identity()

    try:
        tour = db.session.get(Tours, tour_id)

        if not tour:
            return jsonify({"error": 'Tour not found!'}), 404

        bookings = Bookings.query.filter_by(user_id=user_id).all()

        for booking in bookings:
            if (
                    tour.start_date <= booking.end_date and
                    tour.end_date >= booking.start_date
                    ):
                return jsonify({'error': 'You have a conflicting tour booked during these dates.'}), 409

        new_booking = Bookings(

