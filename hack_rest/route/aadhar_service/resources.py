from http import HTTPStatus
from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource

from hack_rest.database import db
from hack_rest.db_models.aadhar_services import AadharService
from hack_rest.route.aadhar_service.models.aadhar_services import (
    AADHAR_RESPONSE_MODEL,
    AADHAR_VALIDATE_MODEL,
)
from hack_rest.route.utils.util_functions import admin_required

AADHAR_SERVICE_NS = Namespace("aadhar_service", description="Aadhar Service APIs")
AADHAR_SERVICE_NS.models[AADHAR_VALIDATE_MODEL.name] = AADHAR_VALIDATE_MODEL
AADHAR_SERVICE_NS.models[AADHAR_RESPONSE_MODEL.name] = AADHAR_RESPONSE_MODEL


@AADHAR_SERVICE_NS.route("/validate")
class AadharValidate(Resource):
    @AADHAR_SERVICE_NS.expect(AADHAR_VALIDATE_MODEL)
    @AADHAR_SERVICE_NS.marshal_with(AADHAR_RESPONSE_MODEL)
    def post(self):
        """Validate Aadhar details"""
        data = request.json
        aadhar = (
            db.session.query(AadharService)
            .filter(AadharService.aadhar_number == data["aadhar_number"])
            .first()
        )
        if not aadhar:
            return {
                "valid": False,
                "message": "Aadhar number not found",
            }, HTTPStatus.NOT_FOUND

        # Simple field match validation
        if (
            aadhar.name == data["name"]
            and aadhar.dob == data["dob"]
            and aadhar.address == data["address"]
            and aadhar.gender == data["gender"]
            and aadhar.mobile_number == data["mobile_number"]
            and aadhar.pan_number == data["pan_number"]
        ):
            return {"valid": True, "message": "Aadhar details validated"}, HTTPStatus.OK

        return {
            "valid": False,
            "message": "Aadhar details do not match",
        }, HTTPStatus.BAD_REQUEST


@AADHAR_SERVICE_NS.route("/register")
class AadharRegister(Resource):
    @AADHAR_SERVICE_NS.expect(AADHAR_VALIDATE_MODEL)
    @AADHAR_SERVICE_NS.marshal_with(AADHAR_RESPONSE_MODEL)
    @admin_required
    def post(self):
        """Register new Aadhar details"""
        data = request.json

        # Check if already exists
        existing = (
            db.session.query(AadharService)
            .filter(AadharService.aadhar_number == data["aadhar_number"])
            .first()
        )
        if existing:
            return {
                "valid": False,
                "message": "Aadhar number already registered",
            }, HTTPStatus.CONFLICT

        try:
            # Convert dob to date if needed
            dob = data["dob"]
            if isinstance(dob, str):
                dob = datetime.strptime(dob, "%Y-%m-%d").date()

            aadhar = AadharService(
                aadhar_number=data["aadhar_number"],
                name=data["name"],
                dob=dob,
                address=data["address"],
                gender=data["gender"],
                mobile_number=data["mobile_number"],
            )
            db.session.add(aadhar)
            db.session.commit()
            return {
                "valid": True,
                "message": "Aadhar registered successfully",
            }, HTTPStatus.CREATED
        except Exception as ex:
            db.session.rollback()
            return {"valid": False, "message": str(ex)}, HTTPStatus.BAD_REQUEST
