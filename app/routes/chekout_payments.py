from flask import Blueprint, request, jsonify, current_app
from app.models import db
from app.models.payments import Pagos
from app.models.historialPagos import HistorialPagos
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
import os

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

# ================= Comprobantes =================
@pagos_bp.route('/subir', methods=['POST'])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
def aprobar_pago(id):
    pago = Pagos.query.get_or_404(id)
    pago.aprobado = True
    try:
        historial = HistorialPagos(pago_id=pago.id, estado='Aprobado')
        db.session.add(historial)
        db.session.commit()
        return jsonify({'mensaje': 'Pago aprobado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/rechazar/<int:id>', methods=['PUT'])
@cross_origin()
def rechazar_pago(id):
    pago = Pagos.query.get_or_404(id)
    pago.aprobado = False
    try:
        historial = HistorialPagos(pago_id=pago.id, estado='Rechazado')
        db.session.add(historial)
        db.session.commit()
        return jsonify({'mensaje': 'Pago rechazado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pagos_bp.route('/historial/<int:pago_id>', methods=['GET'])
@cross_origin()
def historial_pago(pago_id):
    historial = HistorialPagos.query.filter_by(pago_id=pago_id).all()
    return jsonify([
        {
            'estado': h.estado,
            'fecha': h.fecha.isoformat()
        } for h in historial
    ])

# ================= Seguimiento =================
@pagos_bp.route('/listar_aprobados', methods=['GET'])
@cross_origin()
def listar_aprobados():
    pagos = Pagos.query.filter_by(aprobado=True).all()
    return jsonify([
        {
            'id': p.id,
            'nombre_cliente': p.nombre_cliente,
            'total': p.total,
            'archivo': p.archivo,
            'estado_envio': getattr(p, 'estado_envio', 'Pago confirmado')
        } for p in pagos
    ])

@pagos_bp.route('/seguimiento/actualizar/<int:pago_id>', methods=['PUT'])
@cross_origin()
def actualizar_seguimiento(pago_id):
    data = request.json
    nuevo_estado = data.get('estado')

    if nuevo_estado not in ['Pago confirmado', 'Enpaquetado', 'Enviado al correo']:
        return jsonify({'error': 'Estado inválido'}), 400

    pago = Pagos.query.get_or_404(pago_id)
    pago.estado_envio = nuevo_estado

    try:
        historial = HistorialPagos(pago_id=pago.id, estado=f'Seguimiento: {nuevo_estado}')
        db.session.add(historial)
        db.session.commit()
        return jsonify({'mensaje': 'Estado actualizado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
