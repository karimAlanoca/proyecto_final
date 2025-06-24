from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='cliente')

    # Relación 1-1 con Cliente
    cliente = db.relationship('Cliente', back_populates='usuario', uselist=False, cascade='all, delete-orphan')
    
    def es_admin(self):
        return self.rol == 'admin'
