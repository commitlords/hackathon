from datetime import datetime
from http import HTTPStatus

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.applications import Application
from hack_rest.route.application.models.application_models import (
    APPLICATION_OUT_MODEL,
    APPLICATION_PUT_MODEL,
    APPLICATION_REGISTER_MODEL,
)
from hack_rest.route.group.common import check_group
from hack_rest.route.utils.custom_errors import UnprocessableError
from hack_rest.route.utils.util_functions import admin_required

APPLICATION_NS = Namespace(
    "applications", description="application register and management"
)

APPLICATION_NS.models[APPLICATION_REGISTER_MODEL.name] = APPLICATION_REGISTER_MODEL
APPLICATION_NS.models[APPLICATION_OUT_MODEL.name] = APPLICATION_OUT_MODEL
APPLICATION_NS.models[APPLICATION_PUT_MODEL.name] = APPLICATION_PUT_MODEL


@APPLICATION_NS.route("")
class ApplicationRegister(Resource):

    @APPLICATION_NS.expect(APPLICATION_REGISTER_MODEL)
    @jwt_required()
    def post(self):
        """register an application"""
        data = request.json
        identity = get_jwt_identity()
        group_id = data["groupID"]
        if identity.get("group_id") != group_id:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN

        if not check_group(group_id):
            return {"message": f"group with {group_id} not found"}, HTTPStatus.NOT_FOUND

        # Check if group already has an active (non-rejected) application
        existing = (
            db.session.query(Application)
            .filter(Application.group_id == group_id)
            .filter(func.upper(Application.status) != "REJECTED")
            .one_or_none()
        )
        if existing:
            return {
                "message": f"This group already has an active application (ID: {existing.id}). "
                "Please wait for review or rejection before creating a new one."
            }, HTTPStatus.UNPROCESSABLE_ENTITY

        user_application = Application(
            group_id=group_id,
            status="IN_PROGRESS",
            loan_amount=data.get("loanAmount"),
            comment=data.get("comment"),
            assigned_to="shg_official@gov.in",
        )

        try:
            db.session.add(user_application)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            raise UnprocessableError("Error in saving application") from err

        return {"applicationID": user_application.id}, HTTPStatus.CREATED

    @admin_required
    @APPLICATION_NS.marshal_list_with(APPLICATION_OUT_MODEL)
    def get(self):
        """get all applications"""
        try:
            applications = db.session.query(Application).all()
            return applications, HTTPStatus.OK
        except SQLAlchemyError as err:
            raise UnprocessableError("Error in fetching application details") from err


@APPLICATION_NS.route("/<int:application_id>/status")
class ApplicationUpdate(Resource):

    @admin_required
    @APPLICATION_NS.expect(APPLICATION_PUT_MODEL)
    def put(self, application_id):
        """update application status"""
        data = request.json
        try:
            application = (
                db.session.query(Application)
                .filter(Application.id == application_id)
                .one_or_none()
            )
            if not application:
                return {
                    "message": f"application {application_id} not found"
                }, HTTPStatus.NOT_FOUND
            application.status = data["status"]
            application.comment = data.get("comment")
            application.updated_at = datetime.now()
            db.session.commit()

        except SQLAlchemyError as err:
            raise UnprocessableError("Error in fetching application details") from err

        return "", HTTPStatus.OK
