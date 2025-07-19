from abc import ABC, abstractmethod
from http import HTTPStatus
from uuid import UUID

from flask_restx import fields
from werkzeug.exceptions import BadRequest

# from hack_rest.database import db
# from hack_rest.db_models.business_categories import BusinessCategory


class ConvertableField(ABC):

    @abstractmethod
    def convert(self, value):
        raise NotImplementedError()


# allowed_choices = lambda: db.session.query(BusinessCategory).all()


class BusinessChoices(fields.String):

    def __init__(self, *args, **kwargs):
        # self.choices = [c.name for c in allowed_choices()]
        self.choices = ["DAIRY", "POULTRY"]
        super().__init__(*args, **kwargs)

    def format(self, value):
        if value not in self.choices:
            raise BadRequest(f"Invalid choice: {value}, must be one of {self.choices}")
        return super().format(value)


class GUID(fields.String, ConvertableField):

    def __init__(self, *args, dashed=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashed = dashed

    def format(self, value):
        return value and (str(value) if self.dashed else value.hex)

    def convert(self, value):
        try:
            return value and UUID(value)
        except (TypeError, ValueError, AttributeError):
            return {"message": f"Invalid GUID value {value}"}, HTTPStatus.BAD_REQUEST


class DateTime(fields.DateTime):
    """custom datetime"""

    def format(self, value):
        dt_str = super().format(value)
        # remove milliseconds
        if "." in dt_str:
            dt_str = dt_str.split(".")[0]
        if "T" in dt_str:
            dt_str = dt_str.replace("T", " ")
        return dt_str
