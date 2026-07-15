from flask import Blueprint, jsonify, request, current_app
import os
import io
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from models import JobPosition, Student, Application, db , Placement
from tasks import student_csv_export
from extensions import cache
student_bp = Blueprint("student", __name__)


@student_bp.route("/student/jobs", methods=["GET"])
@cache.cached(timeout=60)
@jwt_required()
@jwt_required()
def get_available_jobs():

    jobs = JobPosition.query.filter_by(
        approval="approved",
        status="active"
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

    job = JobPosition.query.get(job_id)

    if job is None:
        return jsonify({
            "message": "Job not found"
        }), 404

    if job.approval != "approved" or job.status != "active":
        return jsonify({
            "message": "This job is no longer available."
        }), 400

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
        print(application.interview_date)
        print(application.interview_mode)
        print(application.feedback)

        data.append({

            "application_id": application.id,
            "job_title": job.title,
            "company": job.company.company_name,
            "status": application.status,
            "applied_on": application.applied_on.strftime("%Y-%m-%d"),

            "interview_date":
                application.interview_date.strftime("%Y-%m-%d %H:%M")
                if application.interview_date else None,

            "interview_mode": application.interview_mode,

            "feedback": application.feedback

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


@student_bp.route("/student/upload_resume", methods=["POST"])
@jwt_required()
def upload_resume():

    print("UPLOAD ROUTE HIT")
    print(request.method)

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    if "resume" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    filename = secure_filename(file.filename)

    upload_path = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_path, exist_ok=True)

    file.save(os.path.join(upload_path, filename))

    student.resume = filename

    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume": filename
    }), 200


@student_bp.route("/student/placements", methods=["GET"])
@jwt_required()
def student_placements():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    placements = Placement.query.filter_by(student_id=student.id).all()

    result = []

    for placement in placements:

            result.append({

        "id": placement.id,

        "company": placement.company.company_name,

        "job_title": placement.job_position.title,

        "placement_date": placement.placement_date.strftime("%d-%m-%Y")

    })

    return jsonify(result), 200

@student_bp.route("/student/offer-letter/<int:placement_id>", methods=["GET"])

def download_offer_letter(placement_id):

    from flask_jwt_extended import decode_token

    token = request.args.get("token")

    if not token:
        return jsonify({
            "message": "Token missing"
        }), 401

    decoded = decode_token(token)

    user_id = decoded["sub"]

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    placement = Placement.query.filter_by(
        id=placement_id,
        student_id=student.id
    ).first()

    if placement is None:
        return jsonify({
            "message": "Placement not found"
        }), 404

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = [

        Paragraph("<b>Placement Portal</b>", styles["Title"]),

        Paragraph("<br/>", styles["Normal"]),

        Paragraph("<b>PLACEMENT OFFER LETTER</b>", styles["Heading2"]),

        Paragraph(f"<b>Student:</b> {student.name}", styles["Normal"]),

        Paragraph(
            f"<b>Company:</b> {placement.company.company_name}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Job Title:</b> {placement.job_position.title}",
            styles["Normal"]
        ),
        Paragraph(
            f"<b>Package:</b> {placement.job_position.salary_package}LPA",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Placement Date:</b> {placement.placement_date.strftime('%d-%m-%Y')}",
            styles["Normal"]
        ),

        Paragraph("<br/>", styles["Normal"]),

        Paragraph(
            "Congratulations! You have successfully secured this placement.",
            styles["BodyText"]
        )

    ]

    doc.build(story)

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=True,

        download_name="Offer_Letter.pdf",

        mimetype="application/pdf"

    )

##########################################
# Student CSV Export
##########################################

@student_bp.route("/student/export-csv", methods=["POST"])
@jwt_required()
def export_student_csv():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    student_csv_export.delay(student.id)

    return jsonify({
        "message": "CSV export started successfully."
    }), 202