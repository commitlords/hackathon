from sqlalchemy import Sequence
from werkzeug.security import check_password_hash, generate_password_hash

from hack_rest.database import db


class Admin(db.Model):
    """admin model"""

    id_seq = Sequence("admin_seq", start=555, increment=111)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    login_id = db.Column("login_id", db.String, unique=True, nullable=False)
    password_hash = db.Column("password_hash", db.String, nullable=False)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)
