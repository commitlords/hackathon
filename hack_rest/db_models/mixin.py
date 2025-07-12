from datetime import datetime

from sqlalchemy import Column, DateTime, String, inspect

# pylint: disable=too-few-public-methods


class PrintMixin:
    """Mixin that adds __str__ and __repr__ functionality to sqlalchemy model"""

    def object_as_str(self):
        return ", ".join(
            f"{c.key}={getattr(self, c.key)}" for c in inspect(self).mapper.column_attrs
        )

    def __str__(self):
        return f"{self.__class__.__name__}({self.object_as_str()})"

    def __repr__(self):
        return self.__str__()


class UpdatedAtByMixin:
    updated_at = Column("updated_at", DateTime, default=datetime.utcnow)
    updated_by = Column("updated_by", String(250))


class CreatedByMixin:
    created_by = Column("created_by", String(250), nullable=False)


class CreatedAtMixin:
    created_at = Column("created_at", DateTime, default=datetime.utcnow, nullable=False)


class ValidToMixin:
    valid_from = Column("valid_from", DateTime, default=datetime.utcnow, nullable=False)
    valid_to = Column("valid_to", DateTime, nullable=True)
