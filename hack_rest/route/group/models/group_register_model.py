from flask_restx import Model, fields

from hack_rest.route.custom_fields.custom_fields import GUID

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
    {
        "interest": fields.String(
            required=True, description="business interest category"
        )
    },
)

GROUP_MEMBER_MODEL = Model(
    "GroupMemberModel",
    {
        "name": fields.String(required=True, description="name of group member"),
        "age": fields.Integer(required=False, description="age of group member"),
        "sex": fields.String(required=False, description="sex of group member"),
        "aadhar": fields.String(
            required=True, description="aadhar no. of group member"
        ),
        "photoID": GUID(description="phot id of the group member"),
    },
)
