from flask_login.mixins import UserMixin
from sqlalchemy.orm import backref
from . import db
from datetime import datetime
# from flask_login import UserMixin


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(150))
#     last_name = db.Column(db.String(150))
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     profile = db.relationship('Profile', backref=db.backref('user'))

# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     graduation_year = db.Column(db.Integer)
#     interests = db.Column(db.String(150))
#     skills = db.Column(db.String(150))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(150))
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(150), unique=True)
    # password = db.Column(db.String(150))
    # graduation_year = db.Column(db.Integer)
    db.relationship('Record', backref=db.backref('student'))

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(150))
    hours = db.Column(db.Integer)
    activity = db.Column(db.String(150))
    supervisor_email = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean(), default=False)
    supervisor_notes = db.Column(db.String(250))
    student_id = db.Column(db.ForeignKey('student.id'))

# class Student(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(150))
#     last_name = db.Column(db.String(150))
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))