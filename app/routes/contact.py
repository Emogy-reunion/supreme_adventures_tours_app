from flask import Blueprint, jsonify, request, render_template
from app import mail, create_app, db
from flask_mail import Message
from app.forms import GuestContactForm, MemberContactForm
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users
from sqlalchemy.orm import selectinload


app = create_app()


contact_bp = Blueprint('contact_bp', __name__)


@contact_bp.route('/guest_contact', methods=['POST'])
def guest_contact():
    '''
    helps logged out users to send emails to admins
    '''
    form = GuestContactForm(data=request.get_json())

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data
    email = form.email.data
    message = form.message.data

    try:
        msg = Message(
                subject='Tour app inquiry',
                sender=app.config['DEFAULT_MAIL_SENDER'],
                recipients=[app.config['DEFAULT_MAIL_SENDER']]
                )
        msg.body = (
                "New inquiry from Tour App:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Message:\n{message}\n"
                )
        msg.html = render_template('guest_contact.html', email=email, name=name, message=message)
        mail.send(msg)
        return jsonify({'success': "Thank you for your message. Our team will get back to you as soon as possible."}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500


@contact_bp.route('/member_contact', methods=['POST'])
@jwt_required()
def member_contact():
    form = MemberContactForm(data=request.get_json())

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    message = form.message.data
    try:
        user_id = get_jwt_identity()
        user = Users.query.options(selectinload(Users.profile)).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': 'User not found!'}), 404

        msg = Message(
                subject='Tour app inquiry',
                sender=app.config['DEFAULT_MAIL_SENDER'],
                recipients=[app.config['DEFAULT_MAIL_SENDER']]
                )
        msg.body = (
                "New inquiry from Tour App:\n\n"
                f"Name: {user.profile.first_name}\n"
                f"Email: {user.email}\n\n"
                f"Message:\n{message}\:n"
                )
        msg.html = render_template('member_contact.html', user=user, message=message)
        mail.send(msg)
        return jsonify({'success': "Thank you for your message. Our team will get back to you as soon as possible."}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
