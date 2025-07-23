from flask_restx import Model, fields

APPLICATION_REGISTER_MODEL = Model(
    "ApplicationRegisterModel",
    {
        "groupID": fields.Integer(
            required=True, description="Group ID of the group", attribute="group_id"
        ),
        "loanAmount": fields.Integer(
            required=True,
            description="Loan Amount of the application",
            attribute="loan_amount",
        ),
        "comment": fields.String(
            required=False, description="Comments for the application"
        ),
    },
)

APPLICATION_OUT_MODEL = APPLICATION_REGISTER_MODEL.clone(
    "applicationOutModel",
    {
        "appicationID": fields.Integer(
            required=True, description="Application ID ID of the group", attribute="id"
        ),
        "groupName": fields.String(
            required=True, description="Group ID of the group", attribute="group.name"
        ),
        "district": fields.String(
            required=True,
            description="district of the group",
            attribute="group.district",
        ),
        "status": fields.String(required=True, description="application status"),
    },
)
