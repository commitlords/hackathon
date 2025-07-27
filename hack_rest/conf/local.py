import os
from datetime import timedelta

ENV = "development"
DEBUG = True

JWT_SECRET_KEY = "JWT_SECRETS"
JWT_IDENTITY_CLAIM = "identity"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=300)

# Local PostgreSQL Configuration
USER = os.environ.get("USER", "docker")
PASSWORD = os.environ.get("PASSWORD", "docker")
HOSTNAME = os.environ.get("DB_HOST", "localhost")
DBNAME = "dhs"

# Remote PostgreSQL Configuration (commented out for local development)
# USER = "postgres"
# PASSWORD = quote_plus("LOKSamarthadmin@123")  # Encodes special characters
# DBNAME = "dhs"
# INSTANCE_CONNECTION_NAME = "hack-team-commit-lords:us-central1:loksamarth"

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Local Database URI
SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOSTNAME}:5432/{DBNAME}"

# Remote Database URI (commented out)
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:LOKSamarthadmin%40123@34.42.184.94:5432/dhs"

# Local Database Binds
SQLALCHEMY_BINDS = {"dhs": f"postgresql://{USER}:{PASSWORD}@{HOSTNAME}:5432/{DBNAME}"}

# Remote Database Binds (commented out)
# SQLALCHEMY_BINDS = {"dhs": "postgresql://postgres:LOKSamarthadmin%40123@34.42.184.94:5432/dhs"}

# SQLAlchemy URI (main database) - Cloud SQL configuration (commented out)
# SQLALCHEMY_DATABASE_URI = (
#     f"postgresql+psycopg2://{USER}:{PASSWORD}@/{DBNAME}"
#     f"?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"
# )

# # SQLAlchemy binds (additional database connections) - Cloud SQL configuration (commented out)
# SQLALCHEMY_BINDS = {
#     "dhs": (
#         f"postgresql+psycopg2://{USER}:{PASSWORD}@/{DBNAME}"
#         f"?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"
#     )
# }

RESTX_ERROR_404_HELP = False
