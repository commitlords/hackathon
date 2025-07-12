from flask_restx import fields
from werkzeug.exceptions import BadRequest

from hack_rest.database import db
from hack_rest.db_models.business_categories import BusinessCategory


class BusinessChoices(fields.String):

    def __init__(self, *args, **kwargs):
        self.choices = [c.name for c in db.session.query(BusinessCategory).all()]
        super().__init__(*args, **kwargs)

    def format(self, value):
        if value not in self.choices:
            raise BadRequest(f"Invalid choice: {value}, must be one of {self.choices}")
        return super().format(value)
