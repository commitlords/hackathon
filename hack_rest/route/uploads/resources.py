from http import HTTPStatus

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
