from app.models import db

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_titular = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    tipo_banco = db.Column(db.String(100), nullable=False)
    nro_cuenta = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)

