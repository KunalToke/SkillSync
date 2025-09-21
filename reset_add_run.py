# reset_and_run.py
import os
from app import app, db

# Database file path (SQLite file in project root)
DB_FILENAME = "career_platform.db"

def reset_database():
    """Delete old DB and create a new one with the updated schema."""
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)
        print(f"🗑 Old database '{DB_FILENAME}' deleted ✅")
    else:
        print("ℹ️ No existing database found, creating fresh one...")

    with app.app_context():
        db.create_all()
        print("✅ New database created successfully with the updated schema!")


if __name__ == "__main__":
    # 1. Reset DB
    reset_database()

    # 2. Run Flask app
    print("🚀 Starting Flask server at http://127.0.0.1:5000/")
    app.run(debug=True)
