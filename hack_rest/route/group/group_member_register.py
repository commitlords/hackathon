from http import HTTPStatus

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.group import GroupMember
from hack_rest.db_models.uploads import AttachmentModel
from hack_rest.route.group.common import check_group
from hack_rest.route.group.models.group_register_model import (
    GROUP_MEMBER_MODEL,
    GROUP_MEMBER_OUTPUT_MODEL,
)
from hack_rest.route.utils.response import parse_json
from hack_rest.route.utils.util_functions import camel_to_snake_case

GROUP_NS = Namespace("groups", description="group member registration and management")

GROUP_NS.models[GROUP_MEMBER_MODEL.name] = GROUP_MEMBER_MODEL
GROUP_NS.models[GROUP_MEMBER_OUTPUT_MODEL.name] = GROUP_MEMBER_OUTPUT_MODEL


@GROUP_NS.route("/<int:group_id>/members")
class AddMember(Resource):

    @jwt_required()
    @GROUP_NS.expect(GROUP_MEMBER_MODEL)
    @parse_json(GROUP_MEMBER_MODEL)
    def post(self, group_id):
        """Add a member to a group"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        data = request.json
        photo_id = data.get("photoID")
        photo = (
            db.session.query(AttachmentModel)
            .filter(AttachmentModel.guid == photo_id)
            .one_or_none()
        )

        if not photo:
            return {"message": "Invalid photo id"}, HTTPStatus.BAD_REQUEST

        try:
            member = GroupMember(
                group_id=group_id,
                name=data.get("name"),
                age=data.get("age"),
                sex=data.get("sex"),
                aadhar_number=data.get("aadharNumber"),
                pan_number=data.get("panNumber"),
                bank_account_number=data.get("bankAccountNumber"),
                bank_ifsc_code=data.get("bankIfscCode"),
                photo_id=data.get("photoID"),
            )
            db.session.add(member)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": f"Error in saving group member: {data.get('name')}",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"member_id": member.id}, HTTPStatus.CREATED

    @jwt_required()
    @GROUP_NS.marshal_with(GROUP_MEMBER_OUTPUT_MODEL)
    def get(self, group_id):
        """get member details of a group"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id and identity.get("role") != "Admin":
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        if not (group := check_group(group_id)):
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        return group.members, HTTPStatus.OK


@GROUP_NS.route("/<int:group_id>/members/<int:member_id>")
class UpdateMember(Resource):

    @jwt_required()
    @GROUP_NS.expect(GROUP_MEMBER_MODEL)
    @parse_json(GROUP_MEMBER_MODEL)
    def put(self, group_id, member_id):
        """update member details of a group"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        if not (group := check_group(group_id)):
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        member = [m for m in group.members if m.id == member_id][0]
        if not member:
            return {
                "message": f"member with {member_id} not found"
            }, HTTPStatus.NOT_FOUND

        data = request.json

        photo_id = data.get("photoID")

        if photo_id:
            photo = (
                db.session.query(AttachmentModel)
                .filter(AttachmentModel.guid == photo_id)
                .one_or_none()
            )

            if not photo:
                return {"message": "Invalid photo id"}, HTTPStatus.BAD_REQUEST

        try:
            for attr in data.keys():
                attr_in_db = camel_to_snake_case(attr)
                setattr(member, attr_in_db, data.get(attr, getattr(member, attr_in_db)))
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": f"Error in saving group member update for {member_id}",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return "", HTTPStatus.OK

    @jwt_required()
    @GROUP_NS.marshal_with(GROUP_MEMBER_OUTPUT_MODEL)
    def get(self, group_id, member_id):
        """get member of a group details"""

        identity = get_jwt_identity()
        if identity.get("group_id") != group_id and identity.get("role") != "Admin":
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        if not (group := check_group(group_id)):
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        member = [m for m in group.members if m.id == member_id][0]
        return member, HTTPStatus.OK

    @jwt_required()
    def delete(self, group_id, member_id):
        """delete a member of a group"""
        identity = get_jwt_identity()
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        if not (group := check_group(group_id)):
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        member = [m for m in group.members if m.id == member_id][0]
        if not member:
            return {
                "message": f"member with {member_id} not found"
            }, HTTPStatus.NOT_FOUND

        try:
            db.session.delete(member)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": f"Error in deleting member {member_id}",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return "", HTTPStatus.NO_CONTENT
