from app import create_app
from app.routes.authentication import auth


app = create_app()
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)
