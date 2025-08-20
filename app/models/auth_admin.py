from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_admin = db.Column(db.String(50), unique=True, nullable=False)
    password_admin = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_admin = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_admin, password)
    
    def __repr__(self):
        return f'<Admin {self.name_admin}>'
    



