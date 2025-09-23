import os
import mercadopago
from flask import Blueprint, request, jsonify

payment_bp = Blueprint("payment", __name__, url_prefix='/payment')
print("MP_ACCESS_TOKEN:", os.getenv("MP_ACCESS_TOKEN"))
sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@payment_bp.route('/create_preference', methods=['POST', 'OPTIONS'])
def create_preference():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight OK'}), 200
    try:
        data = request.json
        print("Data recibida:", data)
        preference_data = {
            "items": [
                {
                    'title': data['title'],
                    'quantity': int(data['quantity']),
                    'unit_price': float(data['unit_price']),
                }
            ],
            'back_urls': {
                'success': 'https://e-commerce-plantilla-frontend.netlify.app/success',
                'failure': 'https://e-commerce-plantilla-frontend.netlify.app/failure',
                'pending': 'https://e-commerce-plantilla-frontend.netlify.app/pending',
            },
            'auto_return': 'approved',
            'payment_methods': {
                'installments': 12
            }
        }
        preference_response = sdk.preference().create(preference_data)
        return jsonify(preference_response['response'])
    except Exception as e:
        print("Error en create_preference:", e)
        return jsonify({'error': str(e)}), 500
