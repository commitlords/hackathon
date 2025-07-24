from flask_restx import Model, fields

from hack_rest.route.custom_fields.custom_fields import GUID, DateTime

GROUP_PUT_MODEL = Model(
    "GroupPutModel",
    {
        "groupName": fields.String(required=True, description="Name of the group"),
        "district": fields.String(required=False, description="District of the group"),
        "password": fields.String(required=True, description="password of the group"),
    },
)
GROUP_INPUT_MODEL = GROUP_PUT_MODEL.clone(
    "GroupInputModel",
    {
        "loginID": fields.String(required=True, description="Login ID of the group"),
        "createdBy": fields.String(
            required=True, description="member who is creating the group"
        ),
    },
)
GROUP_LOGIN_MODEL = Model(
    "GroupLoginModel",
    {
        "loginID": fields.String(required=True, description="Login ID of the group"),
        "password": fields.String(required=True, description="password of the group"),
    },
)

GROUP_INTEREST_MODEL = Model(
    "GroupInterestModel",
    {"name": fields.String(required=True, description="business interest category")},
)

GROUP_MEMBER_MODEL = Model(
    "GroupMemberModel",
    {
        "name": fields.String(required=True, description="name of group member"),
        "age": fields.Integer(required=False, description="age of group member"),
        "sex": fields.String(required=False, description="sex of group member"),
        "aadharNumber": fields.String(
            required=True,
            description="Aadhar no. of group member",
            attribute="aadhar_number",
        ),
        "panNumber": fields.String(
            required=True, description="PAN no. of group member", attribute="pan_number"
        ),
        "bankAccountNumber": fields.String(
            required=True,
            description="Bank account no. of group member",
            attribute="bank_account_number",
        ),
        "bankIfscCode": fields.String(
            required=True,
            description="Bank IfSC code of group member",
            attribute="bank_ifsc_code",
        ),
        "photoID": GUID(
            description="phot id of the group member", attribute="photo_id"
        ),
    },
)

GROUP_MEMBER_OUTPUT_MODEL = GROUP_MEMBER_MODEL.clone(
    "GroupMemberOut",
    {
        "createdAt": DateTime(
            required=True, description="group member created_at", attribute="created_at"
        ),
        "updatedAt": DateTime(
            required=True, description="group member updated_at", attribute="updated_at"
        ),
    },
)

APPLICATION_DETAIL_MODEL = Model(
    "ApplicationDetails",
    {
        "applicationID": fields.Integer(description="application ID", attribute="id"),
        "status": fields.String(description="Application Status"),
        "loanAmount": fields.String(
            description="Application Loan Amount", attribute="loan_amount"
        ),
    },
)

GROUP_OUTPUT_MODEL = Model(
    "GroupOutputModel",
    {
        "groupName": fields.String(
            required=True, description="Name of the group", attribute="name"
        ),
        "district": fields.String(required=False, description="District of the group"),
        "loginID": fields.String(
            required=True, description="Login ID of the group", attribute="login_id"
        ),
        "createdBy": fields.String(
            required=True,
            description="member who is creating the group",
            attribute="created_by",
        ),
        "createdAt": DateTime(
            required=True, description="group created_at", attribute="created_at"
        ),
        "updatedAt": DateTime(
            required=True, description="group created_at", attribute="updated_at"
        ),
        "members": fields.List(
            fields.Nested(GROUP_MEMBER_OUTPUT_MODEL), description="members of group"
        ),
        "interests": fields.List(
            fields.Nested(GROUP_INTEREST_MODEL), description="group interest"
        ),
        "applications": fields.List(
            fields.Nested(APPLICATION_DETAIL_MODEL), description="application details"
        ),
    },
)
