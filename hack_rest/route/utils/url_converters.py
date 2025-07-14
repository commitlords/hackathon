from uuid import UUID

from werkzeug.exceptions import BadRequest
from werkzeug.routing import BaseConverter


class GUIDConverter(BaseConverter):

    def to_python(self, value: str) -> UUID:
        try:
            return None if value == "null" else UUID(value)
        except (ValueError, TypeError, AttributeError) as error:
            raise BadRequest(f"{value} is not a GUID") from error

    def to_url(self, value: UUID) -> str:
        return super().to_url(value.hex if value is not None else "null")
