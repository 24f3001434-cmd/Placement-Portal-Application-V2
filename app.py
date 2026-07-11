from flask import Flask
from models import db, User
from datetime import timedelta

from extensions import bcrypt
from flask_jwt_extended import JWTManager

from controllers.auth import auth_bp
from controllers.admin import admin_bp

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bcrypt.init_app(app)

jwt = JWTManager(app)



app.config["SECRET_KEY"] = "Ronit1806"
app.config["JWT_SECRET_KEY"] = "RonitJWT1806"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


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
    

if __name__ == "__main__":
    app.run(debug=True)