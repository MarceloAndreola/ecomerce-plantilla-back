from app.models import db
from datetime import datetime

class Pagos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    archivo = db.Column(db.String(200), nullable=False)  # ruta del comprobante
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    aprobado = db.Column(db.Boolean, default=False)  # para que admin lo apruebe
