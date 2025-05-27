from app import create_app
from app.models import db, bcrypt, Users, Profiles
from app.background.verification_email import mail
from flask_jwt_extended import JWTManager
from app.routes.authentication import auth
from app.routes.email_verification import verify
from app.routes.reset_password import reset
import os
from flask_cors import CORS
from app.celery import make_celery
from app.utils.create_initial_admin import create_initial_admin
from app.routes.upload import post
from app.utils.create_upload_folder import create_upload_folder



app = create_app()
jwt = JWTManager(app)
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
celery = make_celery(app)

if app.config["ENV"] == "development":
    CORS(app)


create_initial_admin()
create_upload_folder()

app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)
app.register_blueprint(post)


if __name__ == "__main__":
    app.run(debug=True)
