from database import db
from flask_login import UserMixin


class Carrito(db.Model):
    __tablename__ ='carito'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    producto = db.relationship('Producto', backref='carrito_items')
    #usuario = db.relationship('Usuario', backref='carrito_items')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # ← corregido

