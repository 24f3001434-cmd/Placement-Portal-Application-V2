from flask import Flask
from models import db, User

app = Flask(__name__)



app.config["SECRET_KEY"] = "Ronit1806"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return "Placement Portal Working"

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@placement.com").first()

    if admin is None:
        admin = User(
            email="admin@placement.com",
            password="admin123",
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
    

if __name__ == "__main__":
    app.run(debug=True)