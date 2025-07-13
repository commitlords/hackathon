from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from hack_rest.database import db
from hack_rest.db_models.db_custom_types import GUID
from hack_rest.db_models.mixin import (
    CreatedAtMixin,
    CreatedByMixin,
    PrintMixin,
    UpdatedAtByMixin,
)
from hack_rest.db_models.uploads import AttachmentModel


class Group(PrintMixin, db.Model, CreatedAtMixin, CreatedByMixin, UpdatedAtByMixin):
    __tablename__ = "groups"
    __bind_key__ = "dhs"

    id_seq = Sequence(name="groups_seq", start=100)
    id = db.Column("group_id", db.Integer, id_seq, primary_key=True)
    name = db.Column("name", db.String, nullable=False, unique=True)
    district = db.Column("district", db.String)
    login_id = db.Column("login_id", db.String, unique=True, nullable=False)
    password_hash = db.Column("password_hash", db.String, nullable=False)
    interests = relationship("GroupBusinessInterest", back_populates="group")
    members = relationship("GroupMember", back_populates="group")

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GroupBusinessInterest(PrintMixin, db.Model):
    __tablename__ = "group_interests"
    __bind_key__ = "dhs"

    group_id = db.Column(
        "group_id",
        db.ForeignKey(Group.id, name="fk_interest_group_id"),
        primary_key=True,
    )
    interest = db.Column("interest", db.String(256))
    group = relationship(Group, back_populates="interests")


class GroupMember(
    PrintMixin, db.Model, CreatedAtMixin, CreatedByMixin, UpdatedAtByMixin
):
    __tablename__ = "group_members"
    __bind_key__ = "dhs"

    id_seq = Sequence("group_member_seq", start=1000)
    id = db.Column("member_id", db.Integer, id_seq, primary_key=True)
    group_id = db.Column(
        "group_id", db.ForeignKey(Group.id, name="fk_grp_mem_group_id")
    )
    name = db.Column("name", db.String, nullable=False)
    age = db.Column("age", db.Integer)
    sex = db.Column("sex", db.String(10))
    aadhar_no = db.Column("aadhar_no", db.String(12), nullable=False)
    photo_id = db.Column(
        "photo_id",
        GUID,
        db.ForeignKey(AttachmentModel.guid, name="fk_grp_mem_photo_id"),
    )
    group = relationship(Group, back_populates="members")
