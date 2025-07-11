from flask import Blueprint
from flask_restx import Api, apidoc

V1_PREFIX = "/api/v1"
api_v1_bp = Blueprint("api_v1", __name__, url_prefix=V1_PREFIX)
api = Api(api_v1_bp,
          title="RESTful webservice for Financial Inclusion",
          version="1.0",
          description="the webservice provides APIs for individual/group onboarding")
apidoc.apidoc.url_prefix = V1_PREFIX