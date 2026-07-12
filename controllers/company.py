from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Company, Student, JobPosition, Application, User

company_bp = Blueprint("company", __name__)

### Post Job####

@company_bp.route("/post-job", methods=["POST"])
@jwt_required()
def post_job():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    data = request.get_json()

    job = JobPosition(
        title=data.get("title"),
        description=data.get("description"),
        eligibility=data.get("eligibility"),
        skills=data.get("skills"),
        experience=data.get("experience"),
        salary_package=data.get("salary_package"),
        company_id=company.id
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job Posted Successfully"
    }), 201

#### JOB Deatails #######

@company_bp.route("/company/jobs", methods=["GET"])
@jwt_required()
def get_company_jobs():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    data = []

    for job in company.job_positions:

        data.append({
            "id": job.id,
            "title": job.title,
            "salary_package": job.salary_package,
            "status": job.approval
        })

    return jsonify(data), 200


@company_bp.route("/company/job/<int:job_id>", methods=["GET"])
@jwt_required()
def get_company_job(job_id):

    job = JobPosition.query.get(job_id)

    if job is None:
        return jsonify({
            "message": "Job not found"
        }), 404

    return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "eligibility": job.eligibility,
        "skills": job.skills,
        "experience": job.experience,
        "salary_package": job.salary_package,
        "status": job.status,
        "approval": job.approval
    }), 200


@company_bp.route("/company/job/<int:job_id>/applications", methods=["GET"])
@jwt_required()
def get_job_applications(job_id):

    applications = Application.query.filter_by(
        job_position_id=job_id
    ).all()

    data = []

    for application in applications:

        student = application.student

        data.append({
            "application_id": application.id,
            "student_id": student.id,
            "student_name": student.name,
            "course": student.course,
            "cgpa": student.cgpa,
            "status": application.status
        })

    return jsonify(data), 200


@company_bp.route("/application/<int:application_id>", methods=["GET"])
@jwt_required()
def get_application(application_id):

    application = Application.query.get(application_id)

    if application is None:

        return jsonify({
            "message": "Application not found"
        }), 404

    student = application.student

    return jsonify({

        "application_id": application.id,
        "student_name": student.name,
        "course": student.course,
        "cgpa": student.cgpa,
        "skills": student.skills,
        "experience": student.experience,
        "status": application.status

    }), 200

##### Applicant Shortlist #####

@company_bp.route("/application/<int:application_id>/shortlist", methods=["PUT"])
@jwt_required()
def shortlist_application(application_id):

    application = Application.query.get(application_id)

    if application is None:

        return jsonify({
            "message": "Application not found"
        }), 404

    application.status = "shortlisted"

    db.session.commit()

    return jsonify({
        "message": "Student shortlisted successfully"
    }), 200

##### Appliacnt reject #####

@company_bp.route("/application/<int:application_id>/reject", methods=["PUT"])
@jwt_required()
def reject_application(application_id):

    application = Application.query.get(application_id)

    if application is None:

        return jsonify({
            "message": "Application not found"
        }), 404

    application.status = "rejected"

    db.session.commit()

    return jsonify({
        "message": "Student rejected successfully"
    }), 200