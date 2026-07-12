from flask import Blueprint, jsonify
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