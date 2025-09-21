from app import app, db

# Run this script once to initialize the database
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
