'''
app entry point
'''
from app import create_app
from app.models import db, bcrypt, Users, Profiles, Tours, TourImages, Products, ProductImages
from app.routes.authentication import auth
from app.routes.email_verification import verify
from app.routes.reset_password import reset
from app.routes.admin_update_uploads import admin_edit_bp
from app.routes.tours import tours_bp
from app.routes.merchandise import merch_bp
from app.routes.search import find
from app.routes.admin_delete import admin_delete_bp
from app.routes.book import book_bp
from app.routes.admin_profile import admin_profile_bp
from app.routes.admin_management import admin_manage_bp
from app.routes.member_profile import member_profile_bp
from app.routes.contact import contact_bp
import os
from flask_cors import CORS
from app.celery import make_celery
from app.utils.create_initial_admin import create_initial_admin
from app.routes.upload import post
from app.utils.create_upload_folder import create_upload_folder


create_upload_folder()
app = create_app()
celery = make_celery(app)


CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

with app.app_context():
    db.create_all()
    create_initial_admin()

#register blueprints
app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(verify, url_prefix='/api')
app.register_blueprint(reset, url_prefix='/api')
app.register_blueprint(post, url_prefix='/api')
app.register_blueprint(admin_edit_bp, url_prefix='/api')
app.register_blueprint(tours_bp, url_prefix='/api')
app.register_blueprint(merch_bp, url_prefix='/api')
app.register_blueprint(find, url_prefix='/api')
app.register_blueprint(admin_delete_bp, url_prefix='/api')
app.register_blueprint(book_bp, url_prefix='/api')
app.register_blueprint(admin_profile_bp, url_prefix='/api')
app.register_blueprint(admin_manage_bp, url_prefix='/api')
app.register_blueprint(member_profile_bp, url_prefix='/api')
app.register_blueprint(contact_bp, url_prefix='/api')


if __name__ == "__main__":
    app.run(debug=True)
