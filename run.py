from app import create_app
from app.routes.authentication import auth
from app.routes.email_verification import verify


app = create_app()
app.register_blueprint(auth)
app.register_blueprint(verify)

if __name__ == "__main__":
    app.run(debug=True)
