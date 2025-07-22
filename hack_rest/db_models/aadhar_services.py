from sqlalchemy import Sequence
from sqlalchemy.orm import validates
from datetime import datetime

from hack_rest.database import db

class AadharService(db.Model):
    """Aadhar Service model"""
    __tablename__ = "aadhar_service"
    __bind_key__ = "dhs"

    id_seq = Sequence("aadhar_service_seq", start=1)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    aadhar_number = db.Column(db.BigInteger, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)  # Date type
    address = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mobile_number = db.Column(db.BigInteger, nullable=False)

    @validates("aadhar_number")
    def validate_aadhar_number(self, key, value):
        value_str = str(value)
        if not value_str.isdigit() or len(value_str) != 12:
            raise ValueError("Aadhar number must be exactly 12 digits.")
        return int(value_str)

    @validates("dob")
    def validate_dob(self, key, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("DOB must be in YYYY-MM-DD format.")
        if value.year < 1900 or value > datetime.today().date():
            raise ValueError("DOB year must be between 1900 and today.")
        return value

    @validates("mobile_number")
    def validate_mobile_number(self, key, value):
        value_str = str(value)
        if not value_str.isdigit() or len(value_str) != 10:
            raise ValueError("Mobile number must be exactly 10 digits.")
        return int(value_str)
