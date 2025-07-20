from sqlalchemy import Sequence

from hack_rest.database import db
from hack_rest.db_models.group import Group


class Application(db.Model):
    __tablename__ = "applications"
    __bind_key__ = "dhs"

    id_seq = Sequence("application_seq", start=1)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    group_id = db.Column(
        "group_id",
        db.ForeignKey(Group.id, name="fk_application_group_id"),
        nullable=False,
    )
    status = db.Column("status", default="SUBMITTED")
    comment = db.Text("comment", nullable=True)
    group = db.relationship(Group, back_populates="applications")
