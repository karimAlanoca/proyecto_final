from database import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    metodo = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)  # ← Asegúrate de tener esto

    #venta = db.relationship('Venta', backref='pago')