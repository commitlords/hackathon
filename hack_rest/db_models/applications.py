from sqlalchemy import Sequence

from hack_rest.database import db


class Application(db.Model):
    __tablename__ = "applications"
    __bind_key__ = "dhs"

    id_seq = Sequence("application_seq", start=179980)
    id = db.Column("id", db.Integer, id_seq, primary_key=True)
    group_id = db.Column(
        "group_id",
        db.ForeignKey("groups.group_id", name="fk_application_group_id"),
        nullable=False,
    )
    status = db.Column("status", db.String(25), default="IN_PROGRESS")
    loan_amount = db.Column("loan_amount", db.Integer)
    comment = db.Column("comment", db.Text, nullable=True)
    assigned_to = db.Column("assigned_to", db.String(35), nullable=True)
    group = db.relationship("Group", back_populates="applications")
