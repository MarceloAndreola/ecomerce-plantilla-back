from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.models import db
import os
from werkzeug.utils import secure_filename


create_users = Blueprint('users', __name__, url_prefix='/user')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#CREAR USUARIOS
@create_users.route('/create-users', methods=['GET','POST'])
def create_user():
    name = request.form.get('name')
    if 'image' not in request.files:
        return jsonify({'error' : 'No se envio imagen'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))

        new_user = User(
            name=name,
            image_path=filename
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'image_path': new_user.image_path
        }), 201
    else:
        return jsonify({'error': 'Archivo no permitido'}), 400
    

@create_users.route('/lista_usuarios', methods=['GET'])
def lista_user():
    usuarios = User.query.all()
    return jsonify([{
        'id' : user.id,
        'name' : user.name,
        'image_path' : user.image_path
    } for user in usuarios])

