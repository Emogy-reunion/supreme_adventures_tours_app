from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Tours, Bookings
from app.utils.mpesa_payment import generate_reference_code, get_access_token, generate_password, send_stk_push


book = Blueprint('book', __name__)

@book.route('/book', methods=['POST'])
@jwt_required()
def book():
    '''
    allows users to book tours
    '''
    tour_id = request.json.get('tour_id')
    user_id = get_jwt_identity()

    form = PhoneNumberForm(date=request.get_json())
    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    phone_number = form.phone_number.data

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

        reference_code = generate_reference_code()

        new_booking = Bookings(
                user_id=user_id,
                tour_id=tour.id,
                tour_name=tour.name,
                amount_paid=tour.final_price,
                start_date=tour.start_date,
                end_date=tour.end_date,
                start_location=tour.start_location,
                destination=tour.destination,
                phone_number=tour.phone_number,
                reference_code=reference_code,
                )
        db.session.add(new_booking)
        db.session.commit()
        response = send_stk_push(tour.final_price, phone_number, reference_code, tour.tour_name)

        if not response.get("ResponseCode") == "0":
            db.session.delete(new_booking)  # delete the pending tour if booking failed
            db.session.commit()
            return jsonify({'error': 'Payment not processed. Please try again!'}), 400

        return jsonify({'success': 'Transaction initiated. Payment is being processed!'}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500
