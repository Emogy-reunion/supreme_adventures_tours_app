from app import create_app
from flask_jwt_extended import JWTManager()
from app.routes.authentication import auth
from app.routes.email_verification import verify
from app.routes.reset_password import reset



app = create_app()
jwt = JWTManager(app)
app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)

if __name__ == "__main__":
    app.run(debug=True)
