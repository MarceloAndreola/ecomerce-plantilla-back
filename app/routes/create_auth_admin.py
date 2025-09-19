from flask import Blueprint, request, jsonify
from app.models import db
from app.models.auth_admin import Admin
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
    create_access_token, 
    create_refresh_token,
    get_jwt
    )
from werkzeug.security import check_password_hash

admin_log = Blueprint('admin', __name__, url_prefix='/admin_auth')

# Almacen simple para tokens revocados (en produccion usar Redis o base de datos)
blacklisted_tokens = set()

@admin_log.record_once
def setup_jwt_callbacks(state):
    jwt = state.app.extensions["flask-jwt-extended"]

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        token_id = jwt_payload['jti'] # JWT ID unico
        return token_id in blacklisted_tokens

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
    
@admin_log.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    token = get_jwt()
    token_id = token["jti"]

    # Agregar el token a la blacklist
    blacklisted_tokens.add(token_id)

    return jsonify({'message' : "Sesion cerrada correctamente"}), 200

@admin_log.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    #Obtener la identidad del token de refresh
    current_user = get_jwt_identity()

    #Crear nuevo token de accesso
    new_access_token = create_access_token(identity=current_user)

    return jsonify({
        'access_token' : new_access_token
    }), 200

