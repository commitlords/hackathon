from flask import Blueprint
from flask_restx import Api, apidoc

from hack_rest.route.group.group_member_register import GROUP_NS as GROUP_NS_2
from hack_rest.route.group.group_register import GROUP_NS
from hack_rest.route.uploads.resources import UPLOADS_NS

V1_PREFIX = "/api/v1"
api_v1_bp = Blueprint("api_v1", __name__, url_prefix=V1_PREFIX)
api_v1 = Api(
    app=api_v1_bp,
    title="RESTful webservice for Financial Inclusion- Group",
    version="1.0",
    description="the webservice provides APIs for individual/group onboarding",
    security="Bearer Auth",
    authorizations={
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT Authorization header using Bearer scheme",
        }
    },
)

apidoc.apidoc.url_prefix = V1_PREFIX

API_V1_NAMESPACES = [GROUP_NS, GROUP_NS_2, UPLOADS_NS]
