from flask import Blueprint, request, jsonify, current_app
from app.models import db
from app.models.payments import Pagos
from app.models.historialPagos import HistorialPagos
from werkzeug.utils import secure_filename
import os

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

@pagos_bp.route('/subir', methods=['POST'])
def subir_comprobante():
    if 'comprobante' not in request.files:
        return jsonify({'error': 'No se envió archivo'}), 400

    file = request.files['comprobante']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo inválido'}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    total = request.form.get('total', 0)
    pago = Pagos(
        nombre_cliente=request.form.get('nombre', 'Anónimo'),
        total=float(total),
        archivo=filename
    )

    try:
        db.session.add(pago)
        db.session.commit()
        return jsonify({'mensaje': 'Comprobante subido correctamente', 'id': pago.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/listar', methods=['GET'])
def listar_pagos():
    pagos = Pagos.query.all()
    return jsonify([{
        'id': p.id,
        'nombre_cliente': p.nombre_cliente,
        'total': p.total,
        'archivo': p.archivo,
        'aprobado': p.aprobado
    } for p in pagos])

@pagos_bp.route('/aprobar/<int:id>', methods=['PUT'])
def aprobar_pago(id):
    pago = Pagos.query.get_or_404(id)
    pago.aprobado = True
    try:
        # Guardar en historial
        historial = HistorialPagos(pago_id=pago.id, estado='Aprobado')
        db.session.add(historial)
        db.session.commit()
        return jsonify({'mensaje': 'Pago aprobado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/rechazar/<int:id>', methods=['PUT'])
def rechazar_pago(id):
    pago = Pagos.query.get_or_404(id)
    pago.aprobado = False
    try:
        # Guardar en historial
        historial = HistorialPagos(pago_id=pago.id, estado='Rechazado')
        db.session.add(historial)
        db.session.commit()
        return jsonify({'mensaje': 'Pago rechazado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@pagos_bp.route('/historial/<int:pago_id>', methods=['GET'])
def historial_pago(pago_id):
    historial = HistorialPagos.query.filter_by(pago_id=pago_id).all()
    return jsonify([
        {
            'estado': h.estado,
            'fecha': h.fecha.isoformat()
        } for h in historial
    ])
