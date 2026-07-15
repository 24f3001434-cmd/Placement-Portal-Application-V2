from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from tasks import monthly_report
from models import db, Company, Student, JobPosition, Application,User,Placement
from extensions import cache
admin_bp = Blueprint("admin", __name__)



##### Admin Dashboard #####


@admin_bp.route("/dashboard", methods=["GET"])
@cache.memoize(timeout=60)
@jwt_required()
def admin_dashboard():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = JobPosition.query.count()
    total_applications = Application.query.count()

    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "jobs": total_jobs,
        "applications": total_applications
    }), 200

### Approve Company ####

@admin_bp.route("/approve-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):

    company = Company.query.get(company_id)

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.approval = "approved"

    db.session.commit()

    return jsonify({
        "message": "Company Approved Successfully"
    }), 200

##### Deactivate Company ######

@admin_bp.route("/deactivate-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def deactivate_company(company_id):

    company = Company.query.get(company_id)

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.approval = "deactivated"

    db.session.commit()

    return jsonify({
        "message": "Company Deactivated Successfully"
    }), 200

###### Remov4e Company #####
@admin_bp.route("/remove-company/<int:company_id>", methods=["DELETE"])
@jwt_required()
def remove_company(company_id):

    company = Company.query.get(company_id)

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    user = User.query.get(company.user_id)

    db.session.delete(company)

    if user:
        db.session.delete(user)

    db.session.commit()

    return jsonify({
        "message": "Company Removed Successfully"
    }), 200

##############################
# All Companies
##############################

@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def get_companies():

    search = request.args.get("search")

    if search:

        companies = Company.query.filter(
            Company.company_name.ilike(f"%{search}%")
        ).all()

    else:

        companies = Company.query.all()

    data = []

    for company in companies:

        data.append({
            "id": company.id,
            "name": company.company_name,
            "industry": company.industry,
            "status": company.approval
        })

    return jsonify(data), 200
##############################
# Single Company Details
##############################
@admin_bp.route("/company/<int:company_id>", methods=["GET"])
@jwt_required()
def get_company(company_id):

    company = Company.query.get(company_id)

    if company is None:
        return jsonify({
            "message": "Company not found"
        }), 404

    return jsonify({
        "id": company.id,
        "name": company.company_name,
        "website": company.website,
        "industry": company.industry,
        "description": company.description,
        "hr_contact": company.hr_contact,
        "status": company.approval
    }), 200


####Job Deatails ####
@admin_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_all_jobs():

    jobs = JobPosition.query.all()

    data = []

    for job in jobs:

        company = Company.query.get(job.company_id)

        data.append({
            "id": job.id,
            "title": job.title,
            "company": company.company_name,
            "salary_package": job.salary_package,
            "status": job.approval
        })

    return jsonify(data), 200



@admin_bp.route("/job/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):

    job = JobPosition.query.get(job_id)

    if job is None:
        return jsonify({
            "message": "Job not found"
        }), 404

    company = Company.query.get(job.company_id)

    return jsonify({
        "id": job.id,
        "company": company.company_name,
        "title": job.title,
        "description": job.description,
        "eligibility": job.eligibility,
        "skills": job.skills,
        "experience": job.experience,
        "salary_package": job.salary_package,
        "status": job.approval
    }), 200


#### Admin Job Approval ####

@admin_bp.route("/approve-job/<int:job_id>", methods=["PUT"])
@jwt_required()
def approve_job(job_id):

    job = JobPosition.query.get(job_id)

    if job is None:
        return jsonify({
            "message": "Job not found"
        }), 404

    job.approval = "approved"

    db.session.commit()

    return jsonify({
        "message": "Job Approved Successfully"
    }), 200

##############################
# Generate Monthly Report
##############################

@admin_bp.route("/monthly-report", methods=["POST"])
@jwt_required()
def generate_monthly_report():

    monthly_report.delay()

    return jsonify({
        "message": "Monthly report generation started."
    }), 202

@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    data = []

    for student in students:

        applications = Application.query.filter_by(
            student_id=student.id
        ).count()

        placements = Placement.query.filter_by(
            student_id=student.id
        ).count()

        data.append({

            "id": student.id,
            "name": student.name,
            "roll_number": student.roll_number,
            "course": student.course,
            "cgpa": student.cgpa,
            "applications": applications,
            "placements": placements

        })

    return jsonify(data), 200

@admin_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_all_applications():

    applications = Application.query.all()

    data = []

    for application in applications:

        data.append({

            "application_id": application.id,

            "student_name": application.student.name,

            "company_name":
                application.job_position.company.company_name,

            "job_title":
                application.job_position.title,

            "status":
                application.status,

            "applied_on":
                application.applied_on.strftime("%d-%m-%Y")

        })

    return jsonify(data), 200

@admin_bp.route("/student/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):

    student = Student.query.get(student_id)

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    applications = []

    for application in student.applications:

        applications.append({

            "job_title": application.job_position.title,
            "company": application.job_position.company.company_name,
            "status": application.status

        })

    placements = []

    student_placements = Placement.query.filter_by(
        student_id=student.id
    ).all()

    for placement in student_placements:

        placements.append({

            "company": placement.company.company_name,
            "job_title": placement.job_position.title,
            "placement_date":
                placement.placement_date.strftime("%d-%m-%Y")

        })

    return jsonify({

        "id": student.id,
        "name": student.name,
        "roll_number": student.roll_number,
        "course": student.course,
        "cgpa": student.cgpa,
        "skills": student.skills,
        "experience": student.experience,
        "resume": student.resume,
        "applications": applications,
        "placements": placements

    }), 200