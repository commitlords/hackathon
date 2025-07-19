from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.business_categories import BusinessCategory
from hack_rest.db_models.group import Group, GroupBusinessInterest
from hack_rest.route.group.common import check_group
from hack_rest.route.group.models.group_register_model import (
    GROUP_INPUT_MODEL,
    GROUP_INTEREST_MODEL,
    GROUP_LOGIN_MODEL,
    GROUP_PUT_MODEL,
)
from hack_rest.route.utils.custom_errors import UnprocessableError

GROUP_NS = Namespace("groups", description="Group registration and management")

GROUP_NS.models[GROUP_INPUT_MODEL.name] = GROUP_INPUT_MODEL
GROUP_NS.models[GROUP_LOGIN_MODEL.name] = GROUP_LOGIN_MODEL
GROUP_NS.models[GROUP_PUT_MODEL.name] = GROUP_PUT_MODEL
GROUP_NS.models[GROUP_INTEREST_MODEL.name] = GROUP_INTEREST_MODEL


def fetch_all_business_categories():
    """fetch names of all business categories"""
    results = db.session.query(BusinessCategory.name).all()
    return [r.name for r in results]


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
        created_by = data.get("createdBy")

        if db.session.query(Group).filter(Group.login_id == login_id).one_or_none():
            return {
                "message": f"LoginID {login_id} already exists"
            }, HTTPStatus.BAD_REQUEST

        if db.session.query(Group).filter(Group.name == group_name).one_or_none():
            return {
                "message": f"Group name {group_name} already exists"
            }, HTTPStatus.BAD_REQUEST

        try:
            group = Group(
                name=group_name,
                district=district,
                login_id=login_id,
                created_by=created_by,
                updated_by=created_by,
            )
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

        access_token = create_access_token(
            identity={"group_id": group.id, "creator": group.created_by}
        )
        return {"access_token": access_token}, HTTPStatus.OK


@GROUP_NS.route("/<int:group_id>/interests")
class AddInterest(Resource):

    @GROUP_NS.expect(GROUP_INTEREST_MODEL)
    @jwt_required()
    def post(self, group_id):
        """register a group interest"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        interest = request.json["interest"]
        try:
            bu_categories = fetch_all_business_categories()
            if interest not in bu_categories:
                raise UnprocessableError(
                    f"interest {interest} not found in business categories"
                )

            group_interest = GroupBusinessInterest(group_id=group_id, name=interest)
            db.session.add(group_interest)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in group interest registration",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"interest": interest}, HTTPStatus.CREATED

    @GROUP_NS.expect(GROUP_INTEREST_MODEL)
    @jwt_required()
    def put(self, group_id):
        """update group interest"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        interest = request.json["interest"]
        try:
            bu_categories = fetch_all_business_categories()
            if interest not in bu_categories:
                raise UnprocessableError(
                    f"interest {interest} not found in business categories"
                )

            group_interest = GroupBusinessInterest(group_id=group_id, name=interest)
            db.session.add(group_interest)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in group interest registration",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"interest": interest}, HTTPStatus.OK


@GROUP_NS.route("/<int:group_id>")
@GROUP_NS.doc(security="Bearer Auth")
class GroupDetail(Resource):

    @jwt_required()
    def get(self, group_id):
        """get group details"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        group = check_group(group_id)
        if not group:
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        return {
            "group_id": group.id,
            "group_name": group.name,
            "district": group.district,
            "interests": [gi.name for gi in group.interests],
        }, HTTPStatus.OK

    @jwt_required()
    def delete(self, group_id):
        """delete a group"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        group = check_group(group_id)
        if not group:
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        try:
            db.session.delete(group)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": f"Error in deleting group {group_id}",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return "", HTTPStatus.NO_CONTENT

    @jwt_required()
    @GROUP_NS.expect(GROUP_PUT_MODEL)
    def put(self, group_id):
        """update a group"""
        data = request.json
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        group_name = data.get("groupName")
        district = data.get("district")
        password = data.get("password")

        group = db.session.query(Group).filter(Group.id == group_id).one_or_none()
        if not group:
            return {
                "message": f"Group {group_id} does not exist"
            }, HTTPStatus.BAD_REQUEST

        try:
            if district:
                group.district = district
            if group_name:
                group.name = group_name
            if password:
                group.set_password(password)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in group update",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"groupID": group.id}, HTTPStatus.OK


@GROUP_NS.route("/<int:group_id>/interests/<string:name>")
class DeleteInterest(Resource):

    @jwt_required()
    def delete(self, group_id, name):
        """delete a group interest"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        if not (group := check_group(group_id)):
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        group_interest = [intrst for intrst in group.interests if intrst.name == name][
            0
        ]
        try:
            db.session.delete(group_interest)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in deleting group interest",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return "", HTTPStatus.NO_CONTENT
