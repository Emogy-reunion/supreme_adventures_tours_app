from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Tours, Bookings, Users
from app.utils.mpesa_payment import generate_reference_code, get_access_token, generate_password, send_stk_push
from app.utils.role import role_required
from app.forms import PhoneNumberForm
from sqlalchemy.orm import selectinload


book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/book', methods=['POST'])
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
        user = db.session.get(Users, user_id)

        if not user and not user.verified:
            return jsonify({'error': 'You must verify your profile before booking a tour.'), 403

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

@book_bp.route('/mpesa_callback', methods=['POST'])
def mpesa_callback():
    try:
        data = request.get_json()

        body = data.get("Body", {}).get("stkCallback", {})
        result_code = body.get("ResultCode")
        result_desc = body.get("ResultDesc")
        reference_code = body.get("AccountReference")
        metadata_items = body.get("CallbackMetadata", {}).get("Item", [])

        booking = Bookings.query.filter_by(reference_code=reference_code).first()

        if not booking:
            return jsonify({"error": "Booking not found for this reference code"}), 404

        if result_code != 0:
            booking.payment_status = 'Failed'
            db.session.commit()
            return jsonify({"error": "Payment failed, please try again"}), 400

        metadata = {item["Name"]: item.get("Value") for item in metadata_items}
        mpesa_receipt = metadata.get("MpesaReceiptNumber")
        phone_number = metadata.get("PhoneNumber")
        amount = metadata.get("Amount")

        booking.amount_paid = amount
        booking.transaction_id = mpesa_receipt
        booking.payment_status = "Success"
        booking.status = "Confirmed"
        db.session.commit()
        return jsonify({"success": "Booking updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        db.session.rollback()
        return jsonify({"error": "Callback handling failed"}), 500

@book_bp.route('/member_bookings', methods=['GET'])
@jwt_required()
def member_bookings():
    try:
        user_id = get_jwt_identity()
        
        bookings = Bookings.query.options(selectinload(Bookings.user)).filter_by(user_id=user_id).all()

        if not bookings:
            return jsonify({'error': 'No available bookings at the moment'}), 404

        booking_details =[{
            'user_name': booking.user.firstname + ' '+ booking.user.last_name,
            'tour_name': booking.tour_name,
            'amount_paid': booking.amount_paid,
            'status': booking.status,
            'payment': booking.payment_status,
            'start_date': booking.start_date.strftime("%B %d, %Y, %I:%M %p"),
            'booking_date': booking.booking_date.strftime("%B %d, %Y, %I:%M %p"),
            } for booking in bookings]
        return jsonify({'booking_details': booking_details})
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


@book_bp.route('/admin_bookings', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_bookings():
    try:
        bookings = Bookings.query.options(selectinload(Bookings.user)).all()

        if not bookings:
            return jsonify({'error': 'No available bookings at the moment'}), 404

        booking_details =[{
            'user_name': f"{booking.user.firstname} {booking.user.last_name}",
            'tour_name': booking.tour_name,
            'amount_paid': booking.amount_paid,
            'status': booking.status,
            'payment': booking.payment_status,
            'reference_code': booking.reference_code,
            'transaction_id': booking.transaction_id,
            'start_date': booking.start_date.strftime("%B %d, %Y, %I:%M %p"),
            'end_date': booking.end_date.strftime("%B %d, %Y, %I:%M %p"),
            'start_location': booking.start_location,
            'destination': booking.destination,
            'phone_number': booking.phone_number,
            'booking_date': booking.booking_date.strftime("%B %d, %Y, %I:%M %p"),
        } for booking in bookings]
        return jsonify({'booking_details': booking_details})
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500
