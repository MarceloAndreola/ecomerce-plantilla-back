import os
import mercadopago
from flask import Blueprint, request, jsonify

payment_bp = Blueprint("payment", __name__)

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@payment_bp.route('create_preference', methods=['POST'])
def create_preference():
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
            'success': 'http://localhost:8080/success',
            'failure': 'http://localhost:8080/failure',
            'pending': 'http://localhost:8080/pending',
        },
        'auto_return': 'approved',
        'payment_methods': {
            'installments': 12
        }
    }
    

    preference_response = sdk.preference().create(preference_data)
    return jsonify(preference_response['response'])