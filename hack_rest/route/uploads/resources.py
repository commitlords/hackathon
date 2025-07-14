from http import HTTPStatus
from uuid import UUID

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import FileStorage

from hack_rest.database import db
from hack_rest.db_models.uploads import AttachmentModel
from hack_rest.route.uploads.models.attachment_model import UPLOADS_MODEL

UPLOADS_NS = Namespace("uploads", description="REST service to upload attachments")

UPLOAD_PARSER = reqparse.RequestParser()
UPLOAD_PARSER.add_argument(
    "attachment", type=FileStorage, location="files", required=True
)

UPLOADS_NS.models[UPLOADS_MODEL.name] = UPLOADS_MODEL

MAX_FILE_SIZE = 20 * 1024 * 1024
ALLOWED_EXTS = ("jpg", "jpeg", "png")


def _if_size_less_than_max(file_obj):
    file_obj.seek(0, 2)  # move to end
    size = file_obj.tell()
    file_obj.seek(0)  # reset back to start

    if size > MAX_FILE_SIZE:
        return False

    return True


@UPLOADS_NS.route("")
class AttachmentUpload(Resource):

    @jwt_required()
    @UPLOADS_NS.expect(UPLOAD_PARSER)
    @UPLOADS_NS.marshal_with(UPLOADS_MODEL)
    def post(self):
        args = UPLOAD_PARSER.parse_args()
        file_obj: FileStorage = args["attachment"]

        if not file_obj:
            return {"message": "No file uploaded"}, HTTPStatus.BAD_REQUEST

        ext = file_obj.filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_EXTS:
            return {"message": "Only JPG and PNG allowed"}, HTTPStatus.BAD_REQUEST

        if not _if_size_less_than_max(file_obj):
            return {
                "message": "File size more than max allowed"
            }, HTTPStatus.BAD_REQUEST

        filename = file_obj.filename
        content = file_obj.stream.read()

        try:
            upload = AttachmentModel(name=filename, content=content)
            db.session.add(upload)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                "message": "Error in saving attachment",
                "details": str(err),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return upload


@UPLOADS_NS.route("/<uuid:guid>")
class AttachmentDownload(Resource):
    @jwt_required()
    def get(self, guid: UUID):
        try:
            attachment = (
                db.session.query(AttachmentModel)
                .filter(AttachmentModel.guid == guid)
                .one_or_none()
            )
            if not attachment:
                return {
                    "message": f"attachment {guid.hex} not found"
                }, HTTPStatus.BAD_REQUEST
            return Response(
                response=attachment.content,
                mimetype="image/jpeg",
                headers={
                    "Content-Disposition": f'inline; filename="{attachment.name}"'
                },
            )
        except SQLAlchemyError as err:
            return {
                "message": "Error in fetching attachment details",
                "detail": str(err),
            }, HTTPStatus.BAD_REQUEST
