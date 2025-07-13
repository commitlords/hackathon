from flask_restx import Model

from hack_rest.route.custom_fields.custom_fields import GUID

UPLOADS_MODEL = Model(
    "Attachment", {"guid": GUID(description="unique identifier for the file")}
)
