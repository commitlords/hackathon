from flask_restx import Model, fields

from hack_rest.route.custom_fields.custom_fields import GUID, DateTime

GROUP_PUT_MODEL = Model(
    "GroupPutModel",
    {
        "groupName": fields.String(required=True, description="Name of the group"),
        "district": fields.String(required=False, description="District of the group"),
        "password": fields.String(required=True, description="password of the group"),
        "groupPhoneNumber": fields.Integer(
            required=True, description="phone number of the group"
        ),
        "email": fields.String(required=True, description="email of the group"),
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
        "dob": fields.String(
            required=True, description="Date Of Birth of group member"
        ),
        "sex": fields.String(required=False, description="sex of group member"),
        "aadharNumber": fields.String(
            required=True,
            description="Aadhar no. of group member",
            attribute="aadhar_number",
        ),
        "panNumber": fields.String(
            required=True, description="PAN no. of group member", attribute="pan_number"
        ),
        "bankName": fields.String(
            required=True,
            description="Bank name in which account resides",
            attribute="bank_name",
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
        "email": fields.String(required=False, description="email of the group member"),
        "phoneNumber": fields.Integer(
            required=False,
            description="phone number of the group member",
            attribute="phone_number",
        ),
        "photoID": GUID(
            description="phot id of the group member", attribute="photo_id"
        ),
    },
)

GROUP_MEMBER_OUTPUT_MODEL = GROUP_MEMBER_MODEL.clone(
    "GroupMemberOut",
    {
        "memberID": fields.Integer(
            required=True, description="Group Member ID", attribute="id"
        ),
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
        "groupID": fields.Integer(
            required=True, description="group id", attribute="id"
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
        "email": fields.String(
            required=False, description="group register email", attribute="email"
        ),
        "groupPhoneNumber": fields.Integer(
            required=True,
            description="group register phone number",
            attribute="group_phone_number",
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
