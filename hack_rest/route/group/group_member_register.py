from http import HTTPStatus

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.group import GroupMember
from hack_rest.db_models.uploads import AttachmentModel
from hack_rest.route.group.models.group_register_model import GROUP_MEMBER_MODEL
from hack_rest.route.utils.response import parse_json

GROUP_NS = Namespace("groups", description="group member registration and management")


@GROUP_NS.route("/groups/<int:group_id>/members")
class AddMember(Resource):

    @jwt_required()
    @GROUP_NS.expect(GROUP_MEMBER_MODEL)
    @parse_json(GROUP_MEMBER_MODEL)
    def post(self, group_id):
        current = get_jwt_identity()
        if current != group_id:
            return {"message", "Unauthorized"}, HTTPStatus.FORBIDDEN

        data = request.json
        photo_id = data.get("photoID")
        photo = (
            db.session.query(AttachmentModel)
            .filter_by(AttachmentModel.guid == photo_id)
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
                aadhar_no=data.get("aadhar_no"),
                photo_id=data.get("photo_id"),
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
