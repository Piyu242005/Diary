"""
Script to create an admin user for the diary application.
Run this once to create the admin account.
"""
from app import create_app, db
from app.models import User

app = create_app()

import os
import traceback

with app.app_context():
    # Force absolute path for database
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'diary.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    print(f"Using Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    try:
        print("Dropping all tables to ensure clean state...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        # Check if admin user already exists (it won't, but keeping logic)
        admin = User.query.filter_by(email='piyu.143247@gmail.com').first()
        
        if admin:
            print("Admin user already exists. Updating password...")
            admin.set_password('Piyu24')
            db.session.commit()
            print("Admin password updated successfully!")
        else:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='piyu.143247@gmail.com'
            )
            admin.set_password('Piyu24')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        print("\nAdmin Login Credentials:")
        print("Email: piyu.143247@gmail.com")
        print("Password: Piyu24")
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
