from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource

from hack_rest.database import db
from hack_rest.db_models.admin import Admin
from hack_rest.route.admin.models.admin_models import ADMIN_LOGIN_MODEL

ADMIN_NS = Namespace("admin", description="Admin functions")

ADMIN_NS.models[ADMIN_LOGIN_MODEL.name] = ADMIN_LOGIN_MODEL


@ADMIN_NS.route("/login")
class AdminLogin(Resource):

    @ADMIN_NS.expect(ADMIN_LOGIN_MODEL)
    def post(self):
        """Admin login"""
        data = request.json
        admin: Admin = (
            db.session.query(Admin).filter(Admin.login_id == data["loginID"]).first()
        )

        if not admin or not admin.check_password(data["password"]):
            return {"message": "Invalid Admin credentials"}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(
            identity={"admin_id": admin.login_id, "role": "Admin"}
        )
        return {"accessToken": access_token}, HTTPStatus.OK
