from flask_restx import Model, fields

GROUP_INPUT_MODEL = Model(
    "GroupInputModel",
    {
        "groupName": fields.String(required=True, description="Name of the group"),
        "district": fields.String(required=False, description="District of the group"),
        "loginID": fields.String(required=True, description="Login ID of the group"),
        "password": fields.String(required=True, description="password of the group"),
    },
)
