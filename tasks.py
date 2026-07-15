from celery_config import celery
from models import Application, Student, Company, JobPosition, Placement
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import csv

EMAIL = "ronitx2005@gmail.com"

PASSWORD = "rrxafxklqnkvbekd"


def send_email(to_email, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    server.send_message(msg)

    server.quit()

@celery.task
def test_task():

    total = Application.query.count()

    print("=" * 50)
    print(f"TOTAL APPLICATIONS : {total}")
    print("=" * 50)

    return total

@celery.task
def interview_reminder():

    tomorrow = datetime.now() + timedelta(days=1)

    applications = Application.query.filter(
        Application.status == "interview",
        Application.interview_date != None
    ).all()

    for application in applications:

        if application.interview_date.date() == tomorrow.date():

            student = application.student
            user = student.user

            company = application.job_position.company.company_name
            job = application.job_position.title

            body = f"""
Hello {student.name},

This is a reminder for your interview.

Company : {company}
Position : {job}
Date : {application.interview_date}
Mode : {application.interview_mode}

Best of Luck!

Placement Portal
"""

            send_email(
                user.email,
                "Interview Reminder",
                body
            )

            print(f"Reminder sent to {user.email}")

    return "Interview reminder job completed."



### command to start celery ###
#####  celery -A celery_worker worker --pool=solo --without-mingle --without-gossip --without-heartbeat --loglevel=info


@celery.task
def monthly_report():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = JobPosition.query.count()
    total_applications = Application.query.count()
    total_placements = Placement.query.count()

    report = f"""
========================================
        MONTHLY PLACEMENT REPORT
========================================

Total Students      : {total_students}
Total Companies     : {total_companies}
Total Jobs          : {total_jobs}
Total Applications  : {total_applications}
Total Placements    : {total_placements}

Generated On : {datetime.now()}

========================================
"""

    with open("reports/admin/monthly_report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print(report)

    return "Monthly report generated successfully."


@celery.task
def company_monthly_report(company_id):

    company = Company.query.get(company_id)

    if company is None:
        return "Company not found"

    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    total_jobs = len(jobs)

    total_applications = 0
    interviews = 0
    selected = 0

    for job in jobs:

        applications = Application.query.filter_by(
            job_position_id=job.id
        ).all()

        total_applications += len(applications)

        interviews += sum(
            1 for application in applications
            if application.status == "interview"
        )

        selected += sum(
            1 for application in applications
            if application.status == "selected"
        )

    report = f"""
========================================
        COMPANY MONTHLY REPORT
========================================

Company Name         : {company.company_name}

Jobs Posted          : {total_jobs}
Applications         : {total_applications}
Interviews Scheduled : {interviews}
Students Selected    : {selected}

Generated On : {datetime.now()}

========================================
"""

    filename = f"reports/company/company_{company.id}_monthly_report.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    print(report)

    return "Company report generated successfully."

@celery.task
def student_csv_export(student_id):

    student = Student.query.get(student_id)

    if student is None:
        return "Student not found"

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    filename = f"reports/student/student_{student.id}_history.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Company",
            "Job Title",
            "Status",
            "Interview Date",
            "Interview Mode"
        ])

        for application in applications:

            writer.writerow([
                application.job_position.company.company_name,
                application.job_position.title,
                application.status,
                application.interview_date.strftime("%d-%m-%Y %H:%M")
                    if application.interview_date else "",
                application.interview_mode or ""
            ])

    send_email(
        student.user.email,
        "CSV Export Completed",
        "Your placement history CSV has been generated successfully."
    )

    print(f"CSV Export completed for {student.user.email}")

    return "Student CSV generated successfully."

@celery.task
def company_csv_export(company_id):

    company = Company.query.get(company_id)

    if company is None:
        return "Company not found"

    applications = (
        Application.query
        .join(JobPosition)
        .join(Student)
        .filter(JobPosition.company_id == company.id)
        .all()
    )

    filename = f"reports/company/company_{company.id}_applications.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student Name",
            "Course",
            "CGPA",
            "Job Title",
            "Status",
            "Interview Date"
        ])

        for application in applications:

            writer.writerow([
                application.student.name,
                application.student.course,
                application.student.cgpa,
                application.job_position.title,
                application.status,
                application.interview_date.strftime("%d-%m-%Y %H:%M")
                if application.interview_date else ""
            ])

    send_email(
        company.user.email,
        "CSV Export Completed",
        "Your company applications CSV has been generated successfully."
    )

    print(f"Company CSV Export completed for {company.user.email}")

    return "Company CSV generated successfully."