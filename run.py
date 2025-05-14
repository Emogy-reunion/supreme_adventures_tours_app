from app import create_app
from app.models import db, Users, Profiles
from flask_jwt_extended import JWTManager
from app.routes.authentication import auth
from app.routes.email_verification import verify
from app.routes.reset_password import reset



app = create_app()
jwt = JWTManager(app)
app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)

with app.app_context:
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
