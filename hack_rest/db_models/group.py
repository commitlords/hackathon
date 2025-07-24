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

# from hack_rest.db_models.applications import Application


class Group(PrintMixin, db.Model, CreatedAtMixin, CreatedByMixin, UpdatedAtByMixin):
    __tablename__ = "groups"
    __bind_key__ = "dhs"

    id_seq = Sequence(name="groups_seq", start=100)
    id = db.Column("group_id", db.Integer, id_seq, primary_key=True)
    name = db.Column("name", db.String, nullable=False, unique=True)
    district = db.Column("district", db.String)
    login_id = db.Column("login_id", db.String, unique=True, nullable=False)
    password_hash = db.Column("password_hash", db.String, nullable=False)
    group_phone_number = db.Column("group_phone_number", db.BigInteger, nullable=False)
    email = db.Column("email", db.String, nullable=True)
    interests = relationship("GroupBusinessInterest", back_populates="group")
    members = relationship("GroupMember", back_populates="group")
    applications = db.relationship("Application", back_populates="group")

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GroupBusinessInterest(PrintMixin, db.Model):
    __tablename__ = "group_interests"
    __bind_key__ = "dhs"

    id_seq = Sequence("group_interest_seq", start=1)
    id = db.Column("group_interest_id", db.Integer, id_seq, primary_key=True)
    group_id = db.Column(
        "group_id",
        db.ForeignKey(Group.id, name="fk_interest_group_id"),
    )
    name = db.Column("name", db.String(256))
    group = relationship(Group, back_populates="interests")


class GroupMember(PrintMixin, db.Model, CreatedAtMixin, UpdatedAtByMixin):
    __tablename__ = "group_members"
    __bind_key__ = "dhs"

    id_seq = Sequence("group_member_seq", start=1000)
    id = db.Column("member_id", db.Integer, id_seq, primary_key=True)
    group_id = db.Column(
        "group_id", db.ForeignKey(Group.id, name="fk_grp_mem_group_id")
    )
    name = db.Column("name", db.String, nullable=False)
    dob = db.Column("dob", db.String, nullable=False)
    sex = db.Column("sex", db.String(10))
    email = db.Column("email", db.String(25), nullable=True)
    phone_number = db.Column("phone_number", db.BigInteger, nullable=True)
    aadhar_number = db.Column("aadhar_number", db.String(12), nullable=False)
    pan_number = db.Column("pan_no", db.String(25), nullable=False)
    bank_name = db.Column("bank_name", db.String(35), nullable=False)
    bank_account_number = db.Column(
        "bank_account_number", db.String(35), nullable=False
    )
    bank_ifsc_code = db.Column("bank_ifsc_code", db.String(35), nullable=False)
    photo_id = db.Column(
        "photo_id",
        GUID,
        db.ForeignKey(AttachmentModel.guid, name="fk_grp_mem_photo_id"),
    )
    group = relationship(Group, back_populates="members")
