from flask_restx import Model, fields
from hack_rest.route.custom_fields.custom_fields import DateTime

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
        "groupInterest": fields.String(required=True, description="Group Interest", attribute="group.interests.0.name"),
        "district": fields.String(
            required=True,
            description="district of the group",
            attribute="group.district",
        ),
        "status": fields.String(required=True, description="application status"),
        "createdAt": DateTime(description="Application Created At", attribute="created_at"),

    },
)

APPLICATION_PUT_MODEL = Model(
    "applicationPutModel",
    {
        "status": fields.String(required=True, description="application status"),
        "comment": fields.String(
            required=False, description="Comments for the application"
        ),
    },
)
