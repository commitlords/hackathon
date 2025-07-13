from functools import wraps
from typing import Optional

from flask import request
from flask_restx import fields
from werkzeug.exceptions import BadRequest

from hack_rest.route.custom_fields.custom_fields import ConvertableField


def parse_json(model, max_list_size: Optional[int] = None, required=True):

    def wrap(func):

        @wraps(func)
        def wrapped_f(*args, **kwargs):
            if not request.is_json:
                if required:
                    raise BadRequest("Payload not found")
                return func(*args, **kwargs)

            def _process_field(model_field, field_value):
                if isinstance(model_field, fields.List):
                    return [
                        _process_field(model_field.container, v) for v in field_value
                    ]
                if isinstance(model_field, fields.Nested):
                    return {
                        k: _process_field(model_field.model.get(k), v)
                        for k, v in field_value.items()
                    }
                if isinstance(model_field, ConvertableField):
                    return model_field.convert(field_value)

                return field_value

            payload = request.json

            def _prepare_payload_item(payload_item: dict):
                if not payload_item and not required:
                    return payload_item

                if not payload_item and required:
                    raise BadRequest("Payload not found")

                for param, value in payload_item.items():
                    field = model.get(param)
                    payload_item[param] = _process_field(field, value)
                return payload_item

            if isinstance(payload, list):
                if max_list_size and len(payload) > max_list_size:
                    raise BadRequest(
                        f"Too many input parameters, Max: {max_list_size}, current: {len(payload)}"
                    )

                # pylint: disable=expression-not-assigned
                [_prepare_payload_item(_) for _ in payload]

            else:
                _prepare_payload_item(payload)

            return func(*args, **kwargs)

        return wrapped_f

    return wrap
