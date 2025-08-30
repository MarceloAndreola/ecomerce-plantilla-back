from flask import Flask, send_from_directory
from app.models import db
from app.models.user import User
from app.routes import main
from app.routes.create_users import create_users
from app.routes.create_prod import create_prod
from app.routes.create_auth_admin import admin_log
from app.routes.bank_details import bank_details
from app.routes.chekout_payments import pagos_bp
from app.models.auth_admin import Admin
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ================= Configuración PostgreSQL =================
# Tomar la URL desde la variable de entorno DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ================= Carpeta para subir comprobantes =================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'comprobantes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================= Inicializar DB =================
db.init_app(app)
with app.app_context():
    db.create_all()

# ================= Registrar Blueprints =================
app.register_blueprint(main)
app.register_blueprint(create_users)
app.register_blueprint(create_prod)
app.register_blueprint(admin_log)
app.register_blueprint(bank_details)
app.register_blueprint(pagos_bp)

# ================= Crear admin si no existe =================
with app.app_context():
    if not Admin.query.filter_by(name_admin="admin").first():
        admin = Admin(name_admin="admin")
        admin.set_password("1234")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin creado: usuario=admin, password=1234")
    else:
        print("⚠️ Admin ya existe")

# ================= Servir archivos subidos =================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ================= Ejecutar app =================
if __name__ == '__main__':
    app.run(debug=True)
