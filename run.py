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
import os
from flask_cors import CORS
from app.celery import make_celery
from app.utils.create_initial_admin import create_initial_admin
from app.routes.upload import post
from app.utils.create_upload_folder import create_upload_folder



app = create_app()
celery = make_celery(app)

if app.config["ENV"] == "development":
    CORS(app)

with app.app_context():
    db.create_all()
    create_initial_admin()

create_upload_folder()

app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)
app.register_blueprint(post)
app.register_blueprint(admin_edit_bp)
app.register_blueprint(tours_bp)
app.register_blueprint(merch_bp)


if __name__ == "__main__":
    app.run(debug=True)
