import re
from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from hack_rest.route.utils.custom_errors import AdminOnly


def camel_to_snake_case(camel_str):
    # Inserts an underscore before any uppercase letter that is preceded by
    # a lowercase letter or digit,
    # then converts the entire string to lowercase.
    s1 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", camel_str)
    return s1.lower()


def admin_required(fn):

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity.get("role").upper() != "ADMIN":
            raise AdminOnly("Admin Access Required")

        return fn(*args, **kwargs)

    return wrapper
