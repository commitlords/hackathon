from flask import Blueprint
from flask_restx import Api, apidoc

from hack_rest.route.group.group_member_register import GROUP_NS as GROUP_NS_2
from hack_rest.route.group.group_register import GROUP_NS

V1_PREFIX = "/api/v1"
api_v1_bp = Blueprint("api_v1", __name__, url_prefix=V1_PREFIX)
api_v1 = Api(
    api_v1_bp,
    title="RESTful webservice for Financial Inclusion- Group",
    version="1.0",
    description="the webservice provides APIs for individual/group onboarding",
)

apidoc.apidoc.url_prefix = V1_PREFIX

API_V1_NAMESPACES = [GROUP_NS, GROUP_NS_2]
