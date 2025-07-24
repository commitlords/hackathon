import os
from datetime import timedelta

ENV = "development"
DEBUG = True

JWT_SECRET_KEY = "JWT_SECRETS"
JWT_IDENTITY_CLAIM = "identity"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)

USER = os.environ.get("USER", "docker")
PASSWORD = os.environ.get("PASSWORD", "docker")
HOSTNAME = os.environ.get("DB_HOST", "localhost")

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOSTNAME}:5432/dhs"
SQLALCHEMY_BINDS = {"dhs": f"postgresql://{USER}:{PASSWORD}@{HOSTNAME}:5432/dhs"}

RESTX_ERROR_404_HELP = False
