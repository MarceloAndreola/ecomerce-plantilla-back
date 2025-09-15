from flask import Blueprint, request, jsonify, current_app
from app.models.product import Productos, Categoria
from app.models import db
import os
from werkzeug.utils import secure_filename
from cloudinary_config import cloudinary, cloudinary_uploader

create_prod = Blueprint('productos', __name__, url_prefix='/productos')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@create_prod.route('/create_prod', methods=['GET', 'POST'])
def create_productos():
    name_prod = request.form.get('name_prod')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    stock = request.form.get('stock')
    categoria_id = request.form.get('categoria_id')

    if not categoria_id:
        return jsonify({'error': 'Falta categoria'}), 400

    if 'image' not in request.files:
        return jsonify({'error' : 'No se envio imagen'}), 400
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({'error' : 'No se seleccionio archivo'}), 400
    
    if file and allowed_file(file.filename):
        resultado = cloudinary.uploader.upload(file)
        url_imagen = resultado['secure_url']

        new_prod = Productos(
            name_prod = name_prod,
            descripcion = descripcion,
            precio = precio,
            stock = stock,
            image_path = url_imagen,
            categoria_id = int(categoria_id)
        )

        db.session.add(new_prod)
        db.session.commit()

        return jsonify({
            'id' : new_prod.id,
            'name_prod' : new_prod.name_prod,
            'descripcion' : new_prod.descripcion,
            'precio' : precio,
            'stock' : stock,
            'image_path' : new_prod.image_path,
            'categoria_id': new_prod.categoria_id
        }), 201
    else:
        return jsonify({'error' : 'Archivo no permitido'}), 400
    

@create_prod.route('/lista_productos', methods=['GET'])
def lista_user():
    producto = Productos.query.all()
    return jsonify([{
        'id' : productos.id,
        'name_prod' : productos.name_prod,
        'descripcion' : productos.descripcion,
        'precio' : productos.precio,
        'stock' : productos.stock,
        'image_path' : productos.image_path
    } for productos in producto])


@create_prod.route('/lista_categorias', methods=["GET"])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([{"id": c.id, "name_cat": c.name_cat} for c in categorias])


@create_prod.route('/lista_prod_por_cat/<int:categoria_id>', methods=["GET"])
def get_prod_por_categoria(categoria_id):
    # Trae todos los productos de la categoría
    productos = Productos.query.filter_by(categoria_id=categoria_id).all()

    # Si no hay productos, devolvemos lista vacía
    if not productos:
        return jsonify([]), 200

    # Armamos la respuesta usando la URL completa de Cloudinary
    return jsonify([
        {
            "id": p.id,
            "name_prod": p.name_prod,
            "descripcion": p.descripcion,
            "precio": p.precio,
            "stock": p.stock,
            "image_path": p.image_path  # ⚡ asumimos que aquí ya está la URL de Cloudinary
        }
        for p in productos
    ]), 200

@create_prod.route('/create_categoria', methods=["POST"])
def create_categoria():
    data = request.get_json()
    name_cat = data.get("name_cat")

    if not name_cat:
        return jsonify({"error": "Falta el nombre de la categoría"}), 400
    
    # Validar que no exista duplicada
    if Categoria.query.filter_by(name_cat=name_cat).first():
        return jsonify({"error": "La categoría ya existe"}), 400

    nueva_cat = Categoria(name_cat=name_cat)
    db.session.add(nueva_cat)
    db.session.commit()

    return jsonify({
        "id": nueva_cat.id,
        "name_cat": nueva_cat.name_cat
    }), 201


@create_prod.route('/buscar_cat/<string:name>', methods=['GET'])
def buscar_cat(name):
    name = name.strip()
    categoria = Categoria.query.filter(Categoria.name_cat.ilike(f"%{name}%")).all()

    if not categoria:
        return jsonify([]), 200
    
    return jsonify([
        {
            'id' : c.id,  
            'name_cat' : c.name_cat,
        }
     for c in categoria
     ]), 200


@create_prod.route('/modificar_cat/<int:id>', methods=['PUT'])
def modificar_cat(id):
    categoria = Categoria.query.get_or_404(id)

    data = request.form

    categoria.name_cat = data.get('name_cat', categoria.name_cat)

    db.session.commit()

    return jsonify({
        'id' : categoria.id,
        'name_cat' : categoria.name_cat
    }), 200

@create_prod.route('/delete_cat/<int:id>', methods=['DELETE'])
def delete_cat(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()

    return jsonify({
        'message' : f'Categoria {id} Nombre: {categoria.name_cat} eliminado con exito'
    })



@create_prod.route('/test', methods=["GET"])
def test():
    return "ok"

@create_prod.route('/buscar_prod/<string:name>', methods=['GET'])
def buscar_prod(name):
    name = name.strip()  # quita espacios
    productos = Productos.query.filter(Productos.name_prod.ilike(f"%{name}%")).all()
    
    if not productos:
        return jsonify([]), 200   # devolvemos lista vacía mejor que error
    
    return jsonify([
        {
            'id': p.id,
            'name_prod': p.name_prod,
            'descripcion': p.descripcion,
            'precio': p.precio,
            'stock': p.stock,
            'categoria_id': p.categoria_id,
            'image_path': p.image_path
        }
        for p in productos
    ]), 200



@create_prod.route('/modificar_prod/<int:id>', methods=['PUT'])
def mod_prod(id):
    producto = Productos.query.get_or_404(id)
    
    data = request.form  # vamos a usar form para archivos opcionales
    file = request.files.get('image')  # puede ser None

    # Actualizamos campos obligatorios
    producto.name_prod = data.get('name_prod', producto.name_prod)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    producto.categoria_id = data.get('categoria_id', producto.categoria_id)

    # Solo actualizamos la imagen si se subió una nueva
    if file and allowed_file(file.filename):
        resultado = cloudinary.uploader.upload(file)
        producto.image_path = resultado['secure_url']

    db.session.commit()

    return jsonify({
        'id': producto.id,
        'name_prod': producto.name_prod,
        'descripcion': producto.descripcion,
        'precio': producto.precio,
        'stock': producto.stock,
        'categoria_id': producto.categoria_id,
        'image_path': producto.image_path
    }), 200

@create_prod.route('/delete_productos/<int:id>', methods=['DELETE'])
def delete_prod(id):
    producto = Productos.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    return jsonify({
        'message': f'Producto {id} Titulo: {producto.name_prod} eliminado con exito'
    }),200


    