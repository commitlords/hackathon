from hack_rest.database import db
from hack_rest.db_models.group import Group


def check_group(group_id):
    """check group"""
    group = db.session.query(Group).filter(Group.id == group_id).one_or_none()
    return group
