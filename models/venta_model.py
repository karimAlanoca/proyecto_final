from database import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'venta'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

    usuario = db.relationship('Usuario', backref='ventas')
    pagos = db.relationship('Pago', backref='venta', cascade='all, delete-orphan')
