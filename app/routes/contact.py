from flask import Blueprint, jsonify, request, render_template
from app import mail, create_app
from flask_mail import Message
from app.forms import GuestContactForm


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
                recipients=[email]
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

