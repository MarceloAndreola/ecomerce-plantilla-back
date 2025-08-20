from flask import Blueprint, request, jsonify
from app.models import db
from app.models.auth_admin import Admin

admin_log = Blueprint('admin', __name__, url_prefix='/admin_auth')

@admin_log.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data or "name_admin" not in data or "password" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    admin = Admin.query.filter_by(name_admin=data["name_admin"]).first()
    if admin and admin.check_password(data["password"]):
        return jsonify({"message": "Login exitoso"}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrecta"}), 401
