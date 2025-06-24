# from database import db

# class Producto(db.Model):
#     __tablename__ = 'productos'
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(100), nullable=False)
#     descripcion = db.Column(db.Text)
#     precio = db.Column(db.Float, nullable=False)
#     stock = db.Column(db.Integer, default=0)
#     activo = db.Column(db.Boolean, default=True)
#     imagen = db.Column(db.String(255))
# models/producto.py
from database import db  # si tienes db separado en database.py

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(255))