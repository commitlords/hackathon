from flask_restx import Model, fields

AADHAR_VALIDATE_MODEL = Model(
    "AadharValidateModel",
    {
        "aadhar_number": fields.String(required=True, description="Aadhar Number"),
        "name": fields.String(required=True, description="Name"),
        "dob": fields.Date(required=True, description="Date of Birth (YYYY-MM-DD)"),
        "address": fields.String(required=True, description="Address"),
        "gender": fields.String(required=True, description="Gender"),
        "mobile_number": fields.Integer(required=True, description="Mobile Number"),
        "pan_number": fields.String(required=False, description="PAN Number"),
    },
)

AADHAR_RESPONSE_MODEL = Model(
    "AadharResponseModel",
    {
        "valid": fields.Boolean(description="Is Aadhar valid"),
        "message": fields.String(description="Validation message"),
    },
)
