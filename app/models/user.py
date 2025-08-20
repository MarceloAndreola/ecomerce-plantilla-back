from app.models import db


class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50)) 
   image_path = db.Column(db.String(255))




   