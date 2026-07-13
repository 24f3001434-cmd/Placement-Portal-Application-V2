from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity


from models import JobPosition, Student, Application, db

student_bp = Blueprint("student", __name__)

@student_bp.route("/student/jobs", methods=["GET"])
@jwt_required()
def get_available_jobs():

    jobs = JobPosition.query.filter_by(
        approval="approved"
    ).all()

    data = []

    for job in jobs:

        data.append({
            "id": job.id,
            "title": job.title,
            "company": job.company.company_name,
            "salary_package": job.salary_package,
            "status": job.status
        })

    return jsonify(data), 200

#### Apply to job #####

@student_bp.route("/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    existing_application = Application.query.filter_by(
        student_id=student.id,
        job_position_id=job_id
    ).first()

    if existing_application:
        return jsonify({
            "message": "You have already applied for this job."
        }), 400

    application = Application(
        student_id=student.id,
        job_position_id=job_id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Application Submitted Successfully"
    }), 201


##### Applied jobs #######

@student_bp.route("/student/applications", methods=["GET"])
@jwt_required()
def get_student_applications():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:

        return jsonify({
            "message": "Student not found"
        }), 404

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    data = []

    for application in applications:

        job = application.job_position

        data.append({

            "application_id": application.id,
            "job_title": job.title,
            "company": job.company.company_name,
            "status": application.status,
            "applied_on": application.applied_on.strftime("%Y-%m-%d")

        })

    return jsonify(data), 200

@student_bp.route("/student/profile", methods=["GET"])
@jwt_required()
def student_profile():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({

        "name": student.name,
        "course": student.course,
        "cgpa": student.cgpa,
        "roll_number": student.roll_number,
        "skills": student.skills,
        "experience": student.experience,
        "resume": student.resume

    }), 200

@student_bp.route("/student/profile", methods=["PUT"])
@jwt_required()
def update_student_profile():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    student.name = data.get("name", student.name)
    student.course = data.get("course", student.course)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.roll_number = data.get("roll_number", student.roll_number)
    student.skills = data.get("skills", student.skills)
    student.experience = data.get("experience", student.experience)
    student.resume = data.get("resume", student.resume)

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200