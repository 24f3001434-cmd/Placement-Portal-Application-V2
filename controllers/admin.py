from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models import db, Company

admin_bp = Blueprint("admin", __name__)


#### Admin Approval Company ####

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