from app.models import db


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_cat = db.Column(db.String(100), nullable=False)
    producto = db.relationship("Productos", backref="categoria", lazy=True)


class Productos(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name_prod = db.Column(db.String(50))
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    
