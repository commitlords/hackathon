import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from hack_rest.api_v1 import API_V1_NAMESPACES, api_v1, api_v1_bp
from hack_rest.api_v2 import API_V2_NAMESPACES, api_v2, api_v2_bp
from hack_rest.database import db
from hack_rest.route.utils.url_converters import GUIDConverter


def configure_namespaces(api_namespaces, api):
    for namespace in api_namespaces:
        api.add_namespace(namespace)


def create_app() -> Flask:
    app = Flask(__name__)
    config_path = os.environ.get(
        "FLASK_CONFIG",
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "conf", "local.py"),
    )
    if config_path:
        app.config.from_pyfile(config_path)

    # Initialize db for current app
    db.init_app(app)

    # Initialize CORS for the current app
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    # Initialize jwt
    JWTManager(app)

    app.url_map.converters["guid"] = GUIDConverter

    app.register_blueprint(api_v1_bp)
    app.register_blueprint(api_v2_bp)

    # Configure available namespaces for this app
    configure_namespaces(API_V1_NAMESPACES, api_v1)
    configure_namespaces(API_V2_NAMESPACES, api_v2)

    return app


if __name__ == "__main__":
    appl = create_app()
    with appl.app_context():
        db.create_all()
    appl.run(host=os.environ.get("FLASK_HOST", "0.0.0.0"), port=8080)
