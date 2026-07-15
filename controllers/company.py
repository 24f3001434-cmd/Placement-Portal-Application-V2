from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db, Company, Student, JobPosition, Application,User,Placement
from tasks import company_monthly_report
from tasks import company_csv_export
from extensions import cache
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
    
    if company.approval != "approved":

        return jsonify({
            "message": "Company is not approved by Admin"
        }), 403

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
        "job_position_id": application.job_position_id,
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

    data = request.get_json()

    application.status = "rejected"
    application.feedback = data.get("feedback", "")

    db.session.commit()

    return jsonify({
        "message": "Student rejected successfully"
    }), 200


### Select Candidate ###
@company_bp.route("/application/<int:application_id>/select", methods=["PUT"])
@jwt_required()
def select_application(application_id):

    application = Application.query.get(application_id)

    if application is None:
        return jsonify({
            "message": "Application not found"
        }), 404

    if application.status == "selected":
        return jsonify({
            "message": "Student already selected"
        }), 400

    data = request.get_json()

    application.status = "selected"
    application.feedback = data.get("feedback", "")

    existing = Placement.query.filter_by(
        application_id=application.id
    ).first()

    if existing is None:

        placement = Placement(
            application_id=application.id,
            student_id=application.student_id,
            company_id=application.job_position.company_id,
            job_position_id=application.job_position_id
        )

        db.session.add(placement)

    db.session.commit()

    return jsonify({
        "message": "Student selected successfully"
    }), 200


#### Close Jobs ####

@company_bp.route("/company/job/<int:job_id>/close", methods=["PUT"])
@jwt_required()
def close_job(job_id):

    job = JobPosition.query.get(job_id)

    if job is None:
        return jsonify({"message": "Job not found"}), 404

    job.status = "closed"

    db.session.commit()

    return jsonify({
        "message": "Job closed successfully"
    }), 200

@company_bp.route("/company/dashboard", methods=["GET"])
@cache.memoize(timeout=60)
@jwt_required()
def company_dashboard():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({"message": "Company not found"}), 404

    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    total_jobs = len(jobs)

    total_applications = 0
    shortlisted = 0

    for job in jobs:

        applications = Application.query.filter_by(
            job_position_id=job.id
        ).all()

        total_applications += len(applications)

        if job.status == "active":

            shortlisted += sum(
                1 for application in applications
                if application.status == "shortlisted"
            )

    return jsonify({

        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "shortlisted": shortlisted

    }), 200

@company_bp.route("/company/applications", methods=["GET"])
@jwt_required()
def get_company_applications():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({"message": "Company not found"}), 404

    applications = (
        Application.query
        .join(JobPosition)
        .filter(JobPosition.company_id == company.id)
        .all()
    )

    data = []

    for application in applications:

        student = application.student
        job = application.job_position

        data.append({
            "application_id": application.id,
            "student_name": student.name,
            "job_title": job.title,
            "status": application.status
        })

    return jsonify(data), 200

#### Company Profile ####

@company_bp.route("/company/profile", methods=["GET"])
@jwt_required()
def company_profile():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({"message": "Company not found"}), 404

    return jsonify({

        "company_name": company.company_name,
        "website": company.website,
        "industry": company.industry,
        "description": company.description,
        "hr_contact": company.hr_contact,
        "approval": company.approval

    }), 200

@company_bp.route("/company/profile", methods=["PUT"])
@jwt_required()
def update_company_profile():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({"message": "Company not found"}), 404

    data = request.get_json()

    company.company_name = data.get("company_name", company.company_name)
    company.website = data.get("website", company.website)
    company.industry = data.get("industry", company.industry)
    company.hr_contact = data.get("hr_contact", company.hr_contact)
    company.description = data.get("description", company.description)

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200

@company_bp.route("/company/shortlisted", methods=["GET"])
@jwt_required()
def company_shortlisted():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({"message": "Company not found"}), 404

    applications = (
        Application.query
        .join(JobPosition)
        .join(Student)
        .filter(
            JobPosition.company_id == company.id,
            Application.status == "shortlisted"
        )
        .all()
    )

    shortlisted = []

    for application in applications:

        shortlisted.append({

            "application_id": application.id,
            "student_name": application.student.name,
            "job_title": application.job_position.title,
            "course": application.student.course,
            "cgpa": application.student.cgpa

        })

    return jsonify(shortlisted), 200


@company_bp.route("/company/application/<int:application_id>/interview", methods=["PUT"])
@jwt_required()
def schedule_interview(application_id):

    data = request.get_json()

    application = Application.query.get(application_id)

    if application is None:

        return jsonify({
            "message": "Application not found"
        }), 404

    application.status = "interview"

    application.interview_date = datetime.fromisoformat(
        data["interview_date"]
    )

    application.interview_mode = data["interview_mode"]
    application.feedback = data.get("feedback", "")

    db.session.commit()

    return jsonify({
        "message": "Interview scheduled successfully"
    }), 200

@company_bp.route("/company/monthly-report", methods=["POST"])
@jwt_required()
def generate_company_monthly_report():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    company_monthly_report.delay(company.id)

    return jsonify({
        "message": "Company monthly report generation started."
    }), 202


##########################################
# Company CSV Export
##########################################

@company_bp.route("/company/export-csv", methods=["POST"])
@jwt_required()
def export_company_csv():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    company_csv_export.delay(company.id)

    return jsonify({
        "message": "Company CSV export started successfully."
    }), 202