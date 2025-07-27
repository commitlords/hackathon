#!/usr/bin/env python3
"""
Script to add admin users to the database
Usage: python add_admin_user.py <username> <password>
"""

import sys
from hack_rest.app import create_app
from hack_rest.database import db
from hack_rest.db_models.admin import Admin

def add_admin_user(username, password):
    """Add an admin user to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = db.session.query(Admin).filter(Admin.login_id == username).first()
        if existing_admin:
            print(f"Admin user '{username}' already exists!")
            return False
        
        # Create new admin
        admin = Admin(login_id=username)
        admin.set_password(password)
        
        try:
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user '{username}' created successfully!")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_admin_user.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    add_admin_user(username, password) 