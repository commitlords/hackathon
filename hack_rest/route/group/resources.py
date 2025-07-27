from flask import request
from flask_restx import Resource, fields, reqparse

from hack_rest.db_models.group import Group as GroupModel
from hack_rest.db_models.group import GroupMember as GroupMemberModel
from hack_rest.database import db

from . import GROUP_NS


def get_all_groups():
    """Get all groups"""
    groups = db.session.query(GroupModel).all()
    return groups


def get_group_by_id(group_id):
    """Get group by ID"""
    return db.session.query(GroupModel).filter_by(id=group_id).first()


def get_group_members(group_id):
    """Get members of a group"""
    return db.session.query(GroupMemberModel).filter_by(group_id=group_id).all()


def add_member_to_group(group_id, member_data):
    """Add member to group"""
    member = GroupMemberModel(group_id=group_id, **member_data)
    db.session.add(member)
    db.session.commit()
    return member


def update_group_member(group_id, member_id, member_data):
    """Update group member"""
    member = db.session.query(GroupMemberModel).filter_by(
        group_id=group_id, id=member_id
    ).first()
    if member:
        for key, value in member_data.items():
            setattr(member, key, value)
        db.session.commit()
    return member


def delete_group_member(group_id, member_id):
    """Delete group member"""
    member = db.session.query(GroupMemberModel).filter_by(
        group_id=group_id, id=member_id
    ).first()
    if member:
        db.session.delete(member)
        db.session.commit()
        return True
    return False

# --- Request Parsers ---
group_parser = reqparse.RequestParser()
group_parser.add_argument("groupName", type=str, help="Name of the group")

member_parser = reqparse.RequestParser()
member_parser.add_argument(
    "name", type=str, required=True, help="Member name cannot be blank"
)
member_parser.add_argument(
    "email", type=str, required=True, help="Member email cannot be blank"
)
# Add other member fields as needed for creation

# --- API Models for Marshalling ---
GROUP_MEMBER_OUTPUT_MODEL = GROUP_NS.model(
    "GroupMemberOutput",
    {
        "memberID": fields.Integer(
            readOnly=True, description="The unique identifier of a member"
        ),
        "name": fields.String(required=True, description="Member name"),
        "dob": fields.String(description="Date of Birth"),
        "sex": fields.String(description="Sex of the member"),
        "phoneNumber": fields.String(description="Phone number"),
        "email": fields.String(required=True, description="Email address"),
        "aadharNumber": fields.String(description="Aadhar card number"),
        "panNumber": fields.String(description="PAN card number"),
        "bankName": fields.String(description="Bank name"),
        "bankAccountNumber": fields.String(description="Bank account number"),
        "bankIfscCode": fields.String(description="Bank IFSC code"),
        "photoID": fields.String(description="ID of the uploaded photo"),
        "createdAt": fields.DateTime(dt_format="iso8601"),
        "updatedAt": fields.DateTime(dt_format="iso8601"),
    },
)

GROUP_MEMBER_INPUT_MODEL = GROUP_NS.model(
    "GroupMemberInput",
    {
        "name": fields.String(required=True, description="Member name"),
        "dob": fields.String(description="Date of Birth"),
        "sex": fields.String(description="Sex of the member"),
        "phone": fields.String(description="Phone number"),
        "email": fields.String(required=True, description="Email address"),
        "aadhar": fields.String(description="Aadhar card number"),
        "pan": fields.String(description="PAN card number"),
        "bankName": fields.String(description="Bank name"),
        "bankAccount": fields.String(description="Bank account number"),
        "ifsc": fields.String(description="Bank IFSC code"),
    },
)


GROUP_OUTPUT_MODEL = GROUP_NS.model(
    "GroupOutput",
    {
        "groupID": fields.Integer(readOnly=True, attribute="id"),
        "groupName": fields.String(required=True, description="Group name"),
        "members": fields.List(fields.Nested(GROUP_MEMBER_OUTPUT_MODEL)),
        "district": fields.String(description="District of the group"),
        "applications": fields.List(
            fields.Nested(
                GROUP_NS.model(
                    "ApplicationSummary",
                    {"applicationID": fields.String, "status": fields.String},
                )
            )
        ),
        "interests": fields.List(
            fields.Nested(GROUP_NS.model("InterestSummary", {"name": fields.String}))
        ),
    },
)

# --- Resources ---


@GROUP_NS.route("")
class GroupListResource(Resource):
    @GROUP_NS.marshal_list_with(GROUP_OUTPUT_MODEL)
    def get(self):
        """List all groups"""
        return get_all_groups()


@GROUP_NS.route("/<int:group_id>")
@GROUP_NS.response(404, "Group not found")
@GROUP_NS.param("group_id", "The group identifier")
class GroupResource(Resource):
    @GROUP_NS.marshal_with(GROUP_OUTPUT_MODEL)
    def get(self, group_id):
        """Fetch a group given its identifier"""
        group = get_group_by_id(group_id)
        if not group:
            GROUP_NS.abort(404)
        return group


@GROUP_NS.route("/<int:group_id>/members")
class GroupMemberListResource(Resource):
    @GROUP_NS.marshal_list_with(GROUP_MEMBER_OUTPUT_MODEL)
    def get(self, group_id: int):
        """Get all members for a specific group"""
        members = get_group_members(group_id)
        return members

    @GROUP_NS.expect(GROUP_MEMBER_INPUT_MODEL)
    def post(self, group_id: int):
        """Add a new member to a group"""
        member_data = request.json
        new_member = add_member_to_group(group_id, member_data)
        if not new_member:
            return {"message": "Group not found or could not add member"}, 404
        return {"message": "Member added successfully", "member": new_member}, 201


@GROUP_NS.route("/<int:group_id>/members/<int:member_id>")
@GROUP_NS.response(404, "Member not found")
class GroupMemberResource(Resource):
    @GROUP_NS.marshal_with(GROUP_MEMBER_OUTPUT_MODEL)
    def get(self, group_id: int, member_id: int):
        """Get a specific member from a group"""
        # This functionality might not be used by the frontend but is good practice to have.
        member = GroupMemberModel.query.filter_by(
            group_id=group_id, id=member_id
        ).first()
        if member:
            return member
        GROUP_NS.abort(
            404, message=f"Member with id {member_id} not found in group {group_id}"
        )

    @GROUP_NS.expect(GROUP_MEMBER_INPUT_MODEL)
    @GROUP_NS.response(200, "Member updated successfully")
    def put(self, group_id: int, member_id: int):
        """Update a group member's details."""
        try:
            member_data = request.get_json()
            updated_member = update_group_member(
                group_id=group_id, member_id=member_id, member_data=member_data
            )
            if not updated_member:
                return {"message": "Member not found or update failed"}, 404

            # Use the output model to serialize the updated member data
            return GROUP_NS.marshal(updated_member, GROUP_MEMBER_OUTPUT_MODEL), 200

        except (ValueError, TypeError) as e:
            print(f"Error updating member: {e}")
            return {
                "message": "Invalid data provided for member update."
            }, 400
        except Exception as e:
            print(f"Unexpected error updating member: {e}")
            return {
                "message": "An internal error occurred while updating the member."
            }, 500

    @GROUP_NS.response(204, "Member deleted successfully")
    def delete(self, group_id: int, member_id: int):
        """Delete a member from a group"""
        if delete_group_member(group_id, member_id):
            return "", 204
        
        return {"message": "Member not found or could not be deleted"}, 404
