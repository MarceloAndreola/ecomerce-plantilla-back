from datetime import datetime
from app.models import db

class HistorialPagos(db.Model):
    __tablename__ = 'historial_pagos'
    
    id = db.Column(db.Integer, primary_key=True)
    pago_id = db.Column(db.Integer, db.ForeignKey('pagos.id'), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    pago = db.relationship('Pagos', backref=db.backref('historial', lazy=True))
