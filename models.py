'''from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class SavedCareer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    career_title = db.Column(db.String(150), nullable=False)
    career_description = db.Column(db.Text, nullable=True)
    skills_required = db.Column(db.String(250), nullable=True)
    growth_scope = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)'''

# models.py
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # renamed field
    user_type = db.Column(db.String(50), nullable=False)  # job_seeker / talent_seeker

    # Relationship → one user can save many careers
    saved_careers = db.relationship("SavedCareer", backref="user", lazy=True)

    # Password helpers
    def set_password(self, password):
        """Hashes the password before saving"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks a plain password against the stored hash"""
        return check_password_hash(self.password_hash, password)


class SavedCareer(db.Model):
    __tablename__ = "saved_career"

    id = db.Column(db.Integer, primary_key=True)
    career_title = db.Column(db.String(150), nullable=False)
    career_description = db.Column(db.Text, nullable=True)
    skills_required = db.Column(db.String(250), nullable=True)
    growth_scope = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
