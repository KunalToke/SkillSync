# reset_db.py
from app import app, db
import os

# Delete old database if exists
db_path = "career_platform.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Old database '{db_path}' deleted ✅")

# Create new database
with app.app_context():
    db.create_all()
    print("New database created with correct schema ✅")
