from flask import Blueprint
from flask_restx import Api, apidoc

V2_PREFIX = "/api/v2"
api_v2_bp = Blueprint("api_v2", __name__, url_prefix=V2_PREFIX)
api_v2 = Api(
    api_v2_bp,
    title="RESTful webservice for Financial Inclusion- Govt",
    version="1.0",
    description="the webservice provides APIs for govt approval",
)

apidoc.apidoc.url_prefix = V2_PREFIX

API_V2_NAMESPACES = []
