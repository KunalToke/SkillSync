# models.py
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # job_seeker / talent_seeker

    # Profile basics
    name = db.Column(db.String(150))
    headline = db.Column(db.String(250))
    about = db.Column(db.Text)
    location = db.Column(db.String(150))
    relocation = db.Column(db.String(50), default="No")
    contact_email = db.Column(db.String(150))
    contact_phone = db.Column(db.String(50))

    # Resume only (profile/cover images are now always default from static/images)
    resume = db.Column(db.String(300))

    # Settings
    visibility = db.Column(db.String(50), default="public")  # public/private/recruiters
    resume_sharing = db.Column(db.Boolean, default=True)

    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    saved_careers = db.relationship("SavedCareer", backref="user", lazy=True)
    skills = db.relationship("Skill", backref="user", cascade="all, delete-orphan")
    education = db.relationship("Education", backref="user", cascade="all, delete-orphan")
    experience = db.relationship("Experience", backref="user", cascade="all, delete-orphan")
    certificates = db.relationship("Certificate", backref="user", cascade="all, delete-orphan")
    job_preferences = db.relationship("JobPreference", backref="user", cascade="all, delete-orphan")

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SavedCareer(db.Model):
    __tablename__ = "saved_career"

    id = db.Column(db.Integer, primary_key=True)
    career_title = db.Column(db.String(150), nullable=False)
    career_description = db.Column(db.Text, nullable=True)
    skills_required = db.Column(db.String(250), nullable=True)
    growth_scope = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# ---------- Extra Tables for Profile ----------

class Skill(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    rating = db.Column(db.Integer)  # 1–5
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(150))
    school = db.Column(db.String(150))
    year = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Experience(db.Model):
    __tablename__ = "experience"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(150))
    company = db.Column(db.String(150))
    duration = db.Column(db.String(100))
    desc = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Certificate(db.Model):
    __tablename__ = "certificate"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    year = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class JobPreference(db.Model):
    __tablename__ = "job_preference"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(150))
    salary = db.Column(db.String(50))
    work_type = db.Column(db.String(50))  # remote / hybrid / onsite
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
