from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.group import Group, GroupBusinessInterest
from hack_rest.route.group.models.group_register_model import (
    GROUP_INPUT_MODEL,
    GROUP_INTEREST_MODEL,
    GROUP_LOGIN_MODEL,
)

GROUP_NS = Namespace("groups", description="Group registration and management")

GROUP_NS.models[GROUP_INPUT_MODEL.name] = GROUP_INPUT_MODEL
GROUP_NS.models[GROUP_LOGIN_MODEL.name] = GROUP_LOGIN_MODEL


@GROUP_NS.route("/register")
class GroupRegister(Resource):
    """register a group"""

    @GROUP_NS.expect(GROUP_INPUT_MODEL)
    def post(self):
        """register a group"""
        data = request.json
        group_name = data.get("groupName")
        district = data.get("district")
        login_id = data.get("loginID")
        password = data.get("password")

        if db.session.query(Group).filter(Group.login_id == login_id).one_or_none():
            return {
                "message": f"LoginID {login_id} already exists"
            }, HTTPStatus.BAD_REQUEST

        if db.session.query(Group).filter(Group.name == group_name).one_or_none():
            return {
                "message": f"Group name {group_name} already exists"
            }, HTTPStatus.BAD_REQUEST

        try:
            group = Group(name=group_name, district=district, login_id=login_id)
            group.set_password(password)
            db.session.add(group)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in group registration",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"groupID": group.id}, HTTPStatus.CREATED


@GROUP_NS.route("/login")
class GroupLogin(Resource):

    @GROUP_NS.expect(GROUP_LOGIN_MODEL)
    def post(self):
        """login a group"""
        data = request.json
        login_id = data.get("loginID")
        password = data.get("password")

        group = db.session.query(Group).filter(Group.login_id == login_id).one_or_none()
        if not group or not group.check_password(password):
            return {"message": "Invalid login ID or password"}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=group.id)
        return {"access_token": access_token}, HTTPStatus.OK


@GROUP_NS.route("/<int:group_id>/interests")
class AddInterest(Resource):

    @GROUP_NS.expect(GROUP_INTEREST_MODEL)
    @jwt_required()
    def post(self, group_id):
        current = get_jwt_identity()
        if current != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        interest = request.json["interest"]
        try:
            group_interest = GroupBusinessInterest(group_id=group_id, interest=interest)
            db.session.add(group_interest)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in group interest registration",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"interest": interest}, HTTPStatus.CREATED
