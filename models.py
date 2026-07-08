from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import backref
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    user = db.relationship("User", backref="admin", uselist=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    cgpa = db.Column(db.Float)
    roll_number = db.Column(db.String(50), unique=True)
    skills = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.Float, nullable=False)
    resume = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)

    user = db.relationship("User", backref="student", uselist=False)
    applications = db.relationship("Application", backref="student", lazy=True)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    industry = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    approval = db.Column(db.String(50), default="pending", nullable=False)
    hr_contact = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)

    user = db.relationship(
        "User",
        backref=backref("company", uselist=False),
        uselist=False
    )
    job_positions = db.relationship("JobPosition", backref="company", lazy=True)


class JobPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    skills = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.Float, nullable=False)
    salary_package = db.Column(db.Float)
    deadline = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="active")
    approval = db.Column(db.String(50), default="pending", nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    applications = db.relationship("Application", backref="job_position", lazy=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default="applied", nullable=False)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    job_position_id = db.Column(db.Integer, db.ForeignKey("job_position.id"), nullable=False)


class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placement_date = db.Column(db.DateTime, default=datetime.utcnow)

    application_id = db.Column(db.Integer, db.ForeignKey("application.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    job_position_id = db.Column(db.Integer, db.ForeignKey("job_position.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    application = db.relationship("Application")
    student = db.relationship("Student")
    job_position = db.relationship("JobPosition")
    company = db.relationship("Company")