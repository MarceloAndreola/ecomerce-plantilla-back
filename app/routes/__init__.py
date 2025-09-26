from flask import Blueprint
# Exportamos todos los blueprints
from .create_users import create_users
from .create_prod import create_prod
from .create_auth_admin import admin_log
from .bank_details import bank_details
from .payment import payment_bp
from .chekout_payments import pagos_bp


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return 'Prueba Flask'