"""Models for Bank related APIs"""
from flask_restx import Model, fields

BANK_ACCOUNT_VALIDATE = Model(
    "BankAccountValidate", {
        "account_number": fields.Integer(required=True),
        "aadhar_number": fields.Integer(required=True),
        "pan_number": fields.String(required=True),
        "ifsc_code": fields.String(required=True),
        "mobile_number": fields.Integer(required=True),
    },
)

BANK_VALIDATE_RESPONSE = Model(
    "BankValidateResponseModel",
    {
        "valid": fields.Boolean(description="Is Aadhar valid"),
        "message": fields.String(description="Validation message"),
    },
)