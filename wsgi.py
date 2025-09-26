from flask import Flask, send_from_directory, jsonify
from app.models import db
from app.models.user import User
from app.models.auth_admin import Admin
from app.routes import main, create_users, create_prod, admin_log, bank_details, payment_bp, pagos_bp
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity
from datetime import timedelta
from config import Config

# ================= Crear app ====================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://e-commerce-plantilla-frontend.netlify.app"}})

# ================= Config ====================
app.config.from_object(Config)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

jwt = JWTManager(app)

# ================= Claims ====================
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    if identity == 'admin':
        return {'role': 'admin', 'permissions': ['read', 'write', 'delete']}
    return {'role': 'user', 'permissions': ['read']}

def is_admin():
    identity = get_jwt_identity()
    if not identity:
        return False
    admin = Admin.query.filter_by(name_admin=identity).first()
    return admin is not None

# ================= JWT Handlers ====================
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token expirado', 'message': 'El token de acceso ha caducado'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Token invalido', 'message': 'La firma del token no es valida'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Token requerido', 'message': 'Se requiere un token de acceso valido'}), 401

# ================= Carpeta uploads ====================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'comprobantes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================= DB ====================
db.init_app(app)
with app.app_context():
    db.create_all()

# ================= Registrar Blueprints ====================
app.register_blueprint(main)
app.register_blueprint(create_users)
app.register_blueprint(create_prod)
app.register_blueprint(admin_log)
app.register_blueprint(bank_details)
app.register_blueprint(pagos_bp)
app.register_blueprint(payment_bp)

# ================= Crear admin ====================
with app.app_context():
    if not Admin.query.filter_by(name_admin="admin").first():
        admin = Admin(name_admin="admin")
        admin.set_password("1234")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin creado: usuario=admin, password=1234")
    else:
        print("⚠️ Admin ya existe")

# ================= Ejecutar app ====================
if __name__ == '__main__':
    app.run(debug=True)
