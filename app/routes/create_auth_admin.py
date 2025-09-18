from flask import Blueprint, request, jsonify
from app.models import db
from app.models.auth_admin import Admin
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
    create_access_token, 
    create_refresh_token
    )
from werkzeug.security import check_password_hash

admin_log = Blueprint('admin', __name__, url_prefix='/admin_auth')

@admin_log.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data or "name_admin" not in data or "password" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    admin = Admin.query.filter_by(name_admin=data["name_admin"]).first()

    if admin and admin.check_password(data["password"]):
        access_token = create_access_token(identity=admin.name_admin)
        refresh_token = create_refresh_token(identity=admin.name_admin)
        return jsonify({
            "message": "Login exitoso",
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            }), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrecta"}), 401
