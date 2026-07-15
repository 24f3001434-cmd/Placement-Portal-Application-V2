from flask import Flask, send_file, jsonify
from models import User,db
from extensions import bcrypt, cache
from datetime import timedelta
from controllers.student import student_bp
from flask_jwt_extended import JWTManager
from extensions import bcrypt, cache
from celery_config import celery
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.company import company_bp

from flask_cors import CORS

app = Flask(__name__)
import os

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)
bcrypt.init_app(app)
cache.init_app(app)


jwt = JWTManager(app)



app.config["SECRET_KEY"] = "Ronit1806"
app.config["JWT_SECRET_KEY"] = "RonitJWT1806"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_DEFAULT_TIMEOUT"] = 60



db.init_app(app)
celery.conf.update(

    broker_url="redis://localhost:6379/0",

    result_backend="redis://localhost:6379/0"

)


class ContextTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with app.app_context():

            return self.run(*args, **kwargs)


celery.Task = ContextTask
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)

@app.route("/")
def home():
    return "Placement Portal Working"

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@placement.com").first()

    if admin is None:
        admin = User(
            email="admin@placement.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()


@app.route("/download-report/<report_type>/<filename>", methods=["GET"])
def download_report(report_type, filename):

    path = os.path.join(
        app.root_path,
        "reports",
        report_type,
        filename
    )

    if not os.path.exists(path):

        return jsonify({
            "message": "Report not found."
        }), 404

    return send_file(
        path,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)