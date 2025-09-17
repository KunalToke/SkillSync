# models/user.py
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# ---------- User Model ----------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="job_seeker")
    company_name = db.Column(db.String(200))
    bio = db.Column(db.Text)
    profile_pic = db.Column(db.String(200), default="/static/images/default-profile.png")
    cover_pic = db.Column(db.String(200), default="/static/images/default-cover.jpg")

    # ✅ Password helpers
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# ---------- Career Save Model ----------
class SavedCareer(db.Model):
    __tablename__ = "saved_careers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    skills = db.Column(db.String(500))
    growth = db.Column(db.String(100))
    salary = db.Column(db.String(100))

    # Relationship (optional)
    user = db.relationship("User", backref="saved_careers")


# ---------- User Functions ----------
def create_user(username, email, password, role="job_seeker", company_name=None):
    """Create a new user with hashed password"""
    user = User(
        username=username,
        email=email,
        role=role,
        company_name=company_name,
    )
    user.set_password(password)  # ✅ hash the password

    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def verify_password(hashed_pw, password):
    """Check hashed password"""
    return check_password_hash(hashed_pw, password)


# ---------- Profile Update Functions ----------
def update_profile(user_id, email=None, bio=None):
    user = User.query.get(user_id)
    if not user:
        return None
    if email:
        user.email = email
    if bio is not None:
        user.bio = bio
    db.session.commit()
    return user


def update_profile_pic(username, url):
    user = get_user_by_username(username)
    if user:
        user.profile_pic = url
        db.session.commit()


def update_cover_pic(username, url):
    user = get_user_by_username(username)
    if user:
        user.cover_pic = url
        db.session.commit()


# ---------- Career Save Functions ----------
def save_career(user_id, title, description, skills, growth, salary):
    career = SavedCareer(
        user_id=user_id,
        title=title,
        description=description,
        skills=skills,
        growth=growth,
        salary=salary,
    )
    db.session.add(career)
    db.session.commit()
    return career


def get_saved_careers(user_id):
    return SavedCareer.query.filter_by(user_id=user_id).all()


def remove_saved_career(career_id, user_id):
    career = SavedCareer.query.filter_by(id=career_id, user_id=user_id).first()
    if career:
        db.session.delete(career)
        db.session.commit()
