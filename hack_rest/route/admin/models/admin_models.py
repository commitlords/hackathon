from flask_restx import Model, fields

ADMIN_LOGIN_MODEL = Model(
    "AdminLoginModel",
    {
        "loginID": fields.String(required=True, description="Login ID of the group"),
        "password": fields.String(required=True, description="password of the group"),
    },
)
