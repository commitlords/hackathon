from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.group import Group
from hack_rest.route.group.models.group_register_model import GROUP_INPUT_MODEL

GROUP_NS = Namespace("groups", description="Group registration and management")

GROUP_NS.models[GROUP_INPUT_MODEL.name] = GROUP_INPUT_MODEL


@GROUP_NS.route("/register")
class GroupRegister(Resource):
    """register a group"""

    @GROUP_NS.expect(GROUP_INPUT_MODEL)
    def post(self):
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
