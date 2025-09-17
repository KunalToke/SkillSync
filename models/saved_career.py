# models/saved_career.py
from extensions import db

class SavedCareer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(250), nullable=False)
    growth = db.Column(db.String(100), nullable=False)
