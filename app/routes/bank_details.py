from flask import Blueprint, jsonify, request
from app.models import db
from app.models.details import Details

bank_details = Blueprint('details', __name__, url_prefix='/details')


# POST inicial: crear los datos bancarios la primera vez
@bank_details.route('/bank_details', methods=['POST'])
def crear_datos_bank():
    data = request.get_json()

    # Validación básica
    required_fields = ['name_titular', 'documento', 'tipo_banco', 'nro_cuenta', 'alias']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Faltan datos'}), 400

    new_details = Details(
        name_titular=data['name_titular'],
        documento=data['documento'],
        tipo_banco=data['tipo_banco'],
        nro_cuenta=data['nro_cuenta'],
        alias=data['alias']
    )

    try:
        db.session.add(new_details)
        db.session.commit()
        return jsonify({
            'id': new_details.id,
            'name_titular': new_details.name_titular,
            'documento': new_details.documento,
            'tipo_banco': new_details.tipo_banco,
            'nro_cuenta': new_details.nro_cuenta,
            'alias': new_details.alias
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bank_details.route('/bank_details/<int:id>', methods=['PUT'])
def modificar_datos_bank(id):
    datos = Details.query.get_or_404(id)
    data = request.get_json()

    # Mantener los valores anteriores si no se envían
    datos.name_titular = data.get('name_titular', datos.name_titular)
    datos.documento = data.get('documento', datos.documento)
    datos.tipo_banco = data.get('tipo_banco', datos.tipo_banco)
    datos.nro_cuenta = data.get('nro_cuenta', datos.nro_cuenta)
    datos.alias = data.get('alias', datos.alias)

    try:
        db.session.commit()
        return jsonify({
            'id': datos.id,
            'name_titular': datos.name_titular,
            'documento': datos.documento,
            'tipo_banco': datos.tipo_banco,
            'nro_cuenta': datos.nro_cuenta,
            'alias': datos.alias
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bank_details.route('/bank_details', methods=['GET'])
def obtener_datos_bank():
    data = Details.query.all()
    print("Registros en DB:", data)
    return jsonify([{
        'id': d.id,
        'name_titular': d.name_titular,
        'documento': d.documento,
        'tipo_banco': d.tipo_banco,
        'nro_cuenta': d.nro_cuenta,
        'alias': d.alias
    } for d in data]), 200



