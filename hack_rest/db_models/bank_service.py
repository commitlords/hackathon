"""Mock Bank Service"""

from hack_rest.database import db


class Bank(db.Model):
    """Banking mock services"""

    __tablename__ = "bank"
    __bind_key__ = "dhs"

    bank_id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(250), nullable=False)


class BankBranch(db.Model):
    """Banking mock services"""

    __tablename__ = "bank_branch"
    __bind_key__ = "dhs"

    branch_id = db.Column(db.Integer, primary_key=True)
    ifsc_code = db.Column(db.String(15), nullable=False)
    branch_address = db.Column(db.String(250), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey("bank.bank_id"), nullable=False)


class BankAccount(db.Model):
    """Banking mock services"""

    __tablename__ = "bank_account"
    __bind_key__ = "dhs"

    account_number = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    aadhar_number = db.Column(db.BigInteger, nullable=False)
    pan_card_number = db.Column(db.String(10), nullable=False)
    account_type = db.Column(db.String(10), nullable=False)
    mobile_number = db.Column(db.Integer, nullable=False)
    email_id = db.Column(db.String(50))
    branch_id = db.Column(
        db.Integer, db.ForeignKey("bank_branch.branch_id"), nullable=False
    )
