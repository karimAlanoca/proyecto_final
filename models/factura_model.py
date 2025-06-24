from database import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)  # 🔹 AGREGA ESTA LÍNEA
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

    cliente = db.relationship('Cliente', backref='facturas')
    venta = db.relationship('Venta', backref='facturas')
    detalles = db.relationship('DetalleFactura', backref='factura', cascade="all, delete-orphan")
