"""Models for Bank related APIs"""

from flask_restx import Model, fields

ADD_BANK_MODEL = Model(
    "AddBankModel",
    {
        "bank_name": fields.String(required=True, description="Bank Name"),
    },
)

ADD_BANK_RESPONSE = Model(
    "AddBankResponseModel",
    {
        "bank_id": fields.Integer(description="Bank ID"),
    },
)


GET_BANK_MODEL = Model(
    "GetBankModel",
    {
        "bank_id": fields.Integer(required=True, description="Bank ID"),
        "bank_name": fields.String(required=True, description="Bank Name"),
    },
)

GET_BANK_BRANCH_MODEL = Model(
    "GetBankBranchModel",
    {
        "bank_id": fields.Integer(required=True, description="Bank ID"),
        "branch_id": fields.Integer(required=True, description="Bank Branch ID"),
        "ifsc_code": fields.String(required=True, description="IFSC Code"),
        "branch_address": fields.String(required=True, description="Branch Address"),
    },
)


ADD_BANK_BRANCH_MODEL = Model(
    "AddBankBranchModel",
    {
        "bank_id": fields.Integer(required=True, description="Bank ID"),
        "account_number": fields.Integer(
            required=True, description="Bank Account Number"
        ),
        "ifsc_code": fields.String(required=True, description="IFSC Code"),
        "branch_address": fields.String(required=True, description="Branch Address"),
    },
)

ADD_BANK_BRANCH_RESPONSE = Model(
    "AddBankBranchResponseModel",
    {
        "branch_id": fields.Integer(description="Bank Branch ID"),
    },
)

GET_BANK_ACCOUNT_MODEL = Model(
    "GetBankAccountModel",
    {
        "account_number": fields.Integer(
            required=True, description="Bank Account Number"
        ),
        "user_name": fields.String(required=True, description="User Name"),
        "balance": fields.Float(required=True, description="Balance"),
        "aadhar_number": fields.Integer(required=True, description="Aadhar Number"),
        "pan_card_number": fields.String(required=True, description="PAN Card Number"),
        "account_type": fields.String(required=True, description="Account Type"),
        "mobile_number": fields.Integer(required=True, description="Mobile Number"),
        "email_id": fields.String(required=True, description="Email ID"),
        "branch_id": fields.Integer(required=True, description="Bank Branch ID"),
    },
)

ADD_BANK_ACCOUNT_MODEL = Model(
    "AddBankAccountModel",
    {
        "account_number": fields.Integer(
            required=True, description="Bank Account Number"
        ),
        "aadhar_number": fields.Integer(required=True, description="Aadhar Number"),
        "pan_card_number": fields.String(required=True, description="PAN Card Number"),
        "user_name": fields.String(required=True, description="User Name"),
        "balance": fields.Float(required=True, description="Balance"),
        "account_type": fields.String(required=True, description="Account Type"),
        "mobile_number": fields.Integer(required=True, description="Mobile Number"),
        "email_id": fields.String(required=True, description="Email ID"),
        "branch_id": fields.Integer(required=True, description="Bank Branch ID"),
    },
)
ADD_BANK_ACCOUNT_RESPONSE = Model(
    "AddBankAccountResponse",
    {
        "account_id": fields.Integer(description="Bank Account ID"),
        "message": fields.String(description="Message"),
    },
)
