from flask import Flask
from flask_restx import Api
from database import db
import os
from flask_jwt_extended import JWTManager


def create_app() -> Flask:
    app = Flask(__name__)
    config_path = os.environ.get("FLASK_CONFIG",
                                 os.path.join(os.path.abspath(os.path.dirname(__file__)), "conf", "local.py"))
    if config_path:
        app.config.from_pyfile(config_path)

    # Initialize db for current app
    db.init_app(app)



