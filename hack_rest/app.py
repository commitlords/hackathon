import logging
import os
from http import HTTPStatus

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import (
    InvalidHeaderError,
    NoAuthorizationError,
    RevokedTokenError,
    WrongTokenError,
)
from jwt import ExpiredSignatureError

from hack_rest.api_v1 import API_V1_NAMESPACES, api_v1, api_v1_bp
from hack_rest.api_v2 import API_V2_NAMESPACES, api_v2, api_v2_bp
from hack_rest.database import db
from hack_rest.route.utils.custom_errors import BaseError
from hack_rest.route.utils.url_converters import GUIDConverter

logger = logging.getLogger(__name__)


def configure_namespaces(api_namespaces, api):
    for namespace in api_namespaces:
        api.add_namespace(namespace)


@click.command("create_db", help="create app related tables")
@with_appcontext
def create_db():
    """create database tables"""
    click.echo("creating app related tables")
    db.create_all()
    click.echo("tables created successfully")


@click.command("drop_db", help="drop app related tables")
@with_appcontext
def drop_db():
    """drop database tables"""
    click.echo("dropping app related tables")
    db.drop_all()
    click.echo("tables dropped successfully")


def register_error_handler(api):
    @api.errorhandler(NoAuthorizationError)
    def handle_no_auth(error):
        return {
            "errorCode": "Authorization Required",
            "message": str(error),
        }, HTTPStatus.FORBIDDEN

    @api.errorhandler(InvalidHeaderError)
    def handle_invalid_header(error):
        return {
            "errorCode": "Invalid Header",
            "message": str(error),
        }, HTTPStatus.FORBIDDEN

    @api.errorhandler(WrongTokenError)
    def handle_wrong_token(error):
        return {"errorCode": "Wrong Token", "message": str(error)}, HTTPStatus.FORBIDDEN

    @api.errorhandler(RevokedTokenError)
    def handle_revoked_token(error):
        return {
            "errorCode": "Revoked Token",
            "message": str(error),
        }, HTTPStatus.FORBIDDEN

    @api.errorhandler(ExpiredSignatureError)
    def handle_expired_signature(error):
        return {
            "errorCode": "Expired Signature",
            "message": str(error),
        }, HTTPStatus.FORBIDDEN

    @api.errorhandler(Exception)
    def handle_generic_error(error):
        logger.exception(f"Error: {str(error)}")
        if isinstance(error, BaseError):
            return {
                "message": getattr(error, "message", "description"),
                "errorCode": getattr(error, "error_code", "PROCESSING_ERROR"),
            }, error.code

        return {
            "message": "Internal Server Error",
            "errorCode": "PROCESSING_ERROR",
        }, HTTPStatus.INTERNAL_SERVER_ERROR


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

    # register_jwt_callbacks(jwt)
    app.url_map.converters["guid"] = GUIDConverter

    app.register_blueprint(api_v1_bp)
    app.register_blueprint(api_v2_bp)

    # Configure available namespaces for this app
    configure_namespaces(API_V1_NAMESPACES, api_v1)
    configure_namespaces(API_V2_NAMESPACES, api_v2)

    # register jwt error handlers
    register_error_handler(api_v1)
    register_error_handler(api_v2)

    # Add cli command options
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)

    return app


if __name__ == "__main__":
    create_app().run(host=os.environ.get("FLASK_HOST", "0.0.0.0"), port=8080)
