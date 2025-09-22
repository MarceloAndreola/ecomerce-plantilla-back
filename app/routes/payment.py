import os
import mercadopago
from flask import Blueprint, request, jsonify, make_response

payment_bp = Blueprint("payment", __name__)

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@payment_bp.route('/create_preference', methods=['POST', 'OPTIONS'])
def create_preference():
    if request.method == 'OPTIONS':
        # Respuesta para preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.json
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