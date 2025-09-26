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


create_users = Blueprint('users', __name__, url_prefix='/user')

# CREAR USUARIOS ADMIN
@create_users.route('/create-users', methods=['POST'])
@jwt_required()
def create_user():
    from wsgi import is_admin
    if not is_admin():
        return jsonify({'msg' : 'No autorizado'}), 403

    data = request.get_json(force=True)  # 🔹 force=True asegura que Flask interprete JSON
    if not data or "name" not in data or "password" not in data:
        return jsonify({'error': 'Faltan datos'}), 400

    # Verificar si el admin ya existe
    existing_user = Admin.query.filter_by(name_admin=data["name"]).first()
    if existing_user:
        return jsonify({'error': 'El usuario ya existe'}), 400

    # Crear admin con password hasheada
    new_user = Admin(
        name_admin=data["name"],
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'name': new_user.name_admin,
        'message': f"Usuario {new_user.name_admin} creado correctamente"  # 🔹 mensaje de confirmación
    }), 201


# LISTAR USUARIOS ADMIN
@create_users.route('/lista_usuarios', methods=['GET'])
@jwt_required(optional=True)
def lista_user():
    usuarios = Admin.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name_admin
    } for user in usuarios])
