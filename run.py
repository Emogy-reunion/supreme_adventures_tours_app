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



app = create_app()
jwt = JWTManager(app)
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
celery = make_celery(app)

if app.config["ENV"] == "development":
    CORS(app)

app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
