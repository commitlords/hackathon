from flask_restx import Model, fields

APPLICATION_REGISTER_MODEL = Model(
    "ApplicationRegisterModel",
    {
        "groupID": fields.Integer(required=True, description="Group ID of the group"),
        "loanAmount": fields.Integer(
            required=True, description="Loan Amount of the application"
        ),
        "comment": fields.String(
            required=False, description="Comments for the application"
        ),
    },
)
