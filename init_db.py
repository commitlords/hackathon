from hack_rest.app import create_app
from hack_rest.database import db

with create_app().app_context():
    db.create_all()