from sqlalchemy import Sequence
from werkzeug.security import check_password_hash, generate_password_hash

from hack_rest.database import db
from hack_rest.db_models.mixin import CreatedAtMixin, CreatedByMixin, PrintMixin


class Group(PrintMixin, db.Model, CreatedAtMixin, CreatedByMixin):
    __tablename__ = "groups"
    __bind_key__ = "dhs"

    id_seq = Sequence(name="groups_seq", start=100)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    name = db.Column("name", db.String, nullable=False, unique=True)
    district = db.Column("district", db.String)
    login_id = db.Column("login_id", db.String, unique=True, nullable=False)
    password_hash = db.Column("password_hash", db.String, nullable=False)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
