from http import HTTPStatus

from flask_restx import Namespace, Resource

from hack_rest.route.common import fetch_all_business_categories

BU_NS = Namespace("business", description="Admin functions")


@BU_NS.route("/interests")
class AllInterest(Resource):

    def get(self, group_id):
        """get all business interests"""
        bu_categories = fetch_all_business_categories()
        return [bu_category.name for bu_category in bu_categories], HTTPStatus.OK
