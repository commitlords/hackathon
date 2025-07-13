import uuid

from hack_rest.database import db
from hack_rest.db_models.db_custom_types import GUID
from hack_rest.db_models.mixin import CreatedAtMixin, PrintMixin


class AttachmentModel(PrintMixin, db.Model, CreatedAtMixin):
    __tablename__ = "attachment"
    __bind_key__ = "dhs"

    guid = db.Column(GUID, default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)
