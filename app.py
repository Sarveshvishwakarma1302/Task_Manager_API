from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv
import os
from models import db
from resources.auth import blp as AuthBlueprint
from resources.task import blp as TaskBlueprint
from resources.user import blp as UserBlueprint


def create_app(config_name=None):

    app = Flask(__name__)
    load_dotenv()
    # Swagger Config
    app.config["API_TITLE"] = "Task Management API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    #  configuration
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["TESTING"] = True
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    JWTManager(app)

    api = Api(app)

    @app.errorhandler(ValidationError)
    def handle_422(err):
        return {
            "message": "Validation Error",
            "errors": err.data.get("messages", [])
        }, 400

    #  Register Blueprints
    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(TaskBlueprint)
    api.register_blueprint(UserBlueprint)

    #  Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)