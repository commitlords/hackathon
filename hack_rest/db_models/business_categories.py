from sqlalchemy import Sequence

from hack_rest.database import db
from hack_rest.db_models.mixin import PrintMixin


class BusinessCategory(PrintMixin, db.Model):
    __tablename__ = "business_categories"
    __bind_key__ = "dhs"

    id_seq = Sequence("business_categories_seq", start=1)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    name = db.Column("name", db.String, unique=True, nullable=False)
    loan_amount = db.Column("loan_amount", db.Integer, nullable=False)
