from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy.exc import SQLAlchemyError

from hack_rest.database import db
from hack_rest.db_models.business_categories import BusinessCategory
from hack_rest.route.business.models.bu_models import BU_INTEREST_MODEL
from hack_rest.route.common import fetch_all_business_categories
from hack_rest.route.utils.custom_errors import UnprocessableError

BU_NS = Namespace("business", description="Business Categories")
BU_NS.models[BU_INTEREST_MODEL.name] = BU_INTEREST_MODEL


@BU_NS.route("/interests")
class BusinessInterest(Resource):

    def get(self):
        """get all business interests"""
        bu_categories = fetch_all_business_categories()
        return bu_categories, HTTPStatus.OK

    @BU_NS.expect([BU_INTEREST_MODEL])
    def post(self):
        """add a business interest category"""
        try:
            for entry in request.json:
                bu = BusinessCategory(
                    name=entry["name"], loan_amount=entry["loanAmount"]
                )
                db.session.add(bu)
                db.session.flush()
        except SQLAlchemyError as err:
            db.session.rollback()
            raise UnprocessableError(
                f"Error in saving interest {entry['name']}"
            ) from err

        db.session.commit()
        return "", HTTPStatus.CREATED


@BU_NS.route("/interests/<string:name>")
class BusinessInterestDel(Resource):

    def delete(self, name):
        """delete a business interest"""
        bu = (
            db.session.query(BusinessCategory)
            .filter(BusinessCategory.name == name)
            .one_or_none()
        )
        if bu:
            db.session.delete(bu)
            db.session.commit()
        return "", HTTPStatus.NO_CONTENT
