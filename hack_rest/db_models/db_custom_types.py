from typing import Any, Optional
from uuid import UUID

from sqlalchemy import Dialect, String, types
from sqlalchemy.sql.operators import OperatorType

# pylint: disable=abstract-method,too-many-ancestors


class GUID(types.TypeDecorator):
    """Custom type for converting btw GUID and database"""

    impl = String(32)
    cache_ok = True

    def process_bind_param(self, value: Optional[UUID], dialect: Dialect) -> str:
        return value.hex if value is not None else None

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[UUID]:
        return UUID(value) if value is not None else None

    def coerce_compared_value(self, op: Optional[OperatorType], value: Any) -> Any:
        return (
            String()
            if isinstance(value, str)
            else super().coerce_compared_value(op, value)
        )
