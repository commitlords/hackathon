import re
from datetime import datetime

from sqlalchemy import Sequence
from sqlalchemy.orm import validates

from hack_rest.database import db


class AadharService(db.Model):
    """Aadhar Service model"""

    __tablename__ = "aadhar_service"
    __bind_key__ = "dhs"

    id_seq = Sequence("aadhar_service_seq", start=1)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    aadhar_number = db.Column(db.String(12), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)  # Date type
    address = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mobile_number = db.Column(db.BigInteger, nullable=False)
    pan_number = db.Column(db.String(10), unique=True, nullable=True)

    @validates("aadhar_number")
    def validate_aadhar_number(self, value):
        if isinstance(value, str) and not value.isdigit() or len(value) != 12:
            raise ValueError("Aadhar number must be exactly 12 digits.")
        return int(value)

    @validates("dob")
    def validate_dob(self, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("DOB must be in YYYY-MM-DD format.")
        if value.year < 1900 or value > datetime.today().date():
            raise ValueError("DOB year must be between 1900 and today.")
        return value

    @validates("mobile_number")
    def validate_mobile_number(self, value):
        value_str = str(value)
        if not value_str.isdigit() or len(value_str) != 10:
            raise ValueError("Mobile number must be exactly 10 digits.")
        return int(value_str)

    @validates("pan_number")
    def validate_pan_number(self, value):
        if value is not None:
            # PAN format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)
            if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", value):
                raise ValueError(
                    "PAN number must be 10 characters: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)."
                )
        return value
