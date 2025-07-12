import os

ENV = "development"
DEBUG = True

JWT_SECRET_KEY = "JWT_SECRETS"

USER = os.environ.get("USER", "docker")
PASSWORD = os.environ.get("PASSWORD", "docker")

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_BINDS = {"dhs": f"postgresql://{USER}:{PASSWORD}@localhost:5432/dhs"}

RESTX_ERROR_404_HELP = False
