from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from models import db, User ,Student , Company
from extensions import bcrypt

auth_bp = Blueprint("auth", __name__)

####  Student registration #####

@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    course = data.get("course")
    cgpa = data.get("cgpa")
    roll_number = data.get("roll_number")
    skills = data.get("skills")
    experience = data.get("experience")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        email=email,
        password=hashed_password,
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    student = Student(
        name=name,
        course=course,
        cgpa=cgpa,
        roll_number=roll_number,
        skills=skills,
        experience=experience,
        user_id=user.id
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student Registered Successfully"
    }), 201


### Student Login #####

@auth_bp.route("/login/student", methods=["POST"])
def login_student():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(
        email=email,
        role="student"
    ).first()

    if user is None:
        return jsonify({
            "message": "Invalid Email"
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid Password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token,
        "role": user.role
    }), 200



#### Admin login ###

@auth_bp.route("/login/admin", methods=["POST"])
def login_admin():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(
        email=email,
        role="admin"
    ).first()

    if user is None:
        return jsonify({
            "message": "Invalid Email"
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid Password"
        }), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Admin Login Successful",
        "access_token": access_token,
        "role": user.role
    }), 200


### Company Registration ####

@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")
    website = data.get("website")
    industry = data.get("industry")
    description = data.get("description")
    hr_contact = data.get("hr_contact")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        email=email,
        password=hashed_password,
        role="company"
    )

    db.session.add(user)
    db.session.commit()

    company = Company(
        company_name=company_name,
        website=website,
        industry=industry,
        description=description,
        hr_contact=hr_contact,
        user_id=user.id
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company Registered Successfully"
    }), 201


### Company login ###

@auth_bp.route("/login/company", methods=["POST"])
def login_company():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(
        email=email,
        role="company"
    ).first()

    if user is None:
        return jsonify({
            "message": "Invalid Email"
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid Password"
        }), 401
    
    company = user.company

    if company.approval != "approved":
        return jsonify({
            "message": "Your account is pending admin approval."
        }), 403

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Company Login Successful",
        "access_token": access_token,
        "role": user.role
    }), 200