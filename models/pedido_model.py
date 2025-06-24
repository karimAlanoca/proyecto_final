from database import db

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(50), nullable=False)  # Ejemplo: 'pendiente', 'enviado', etc.
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=True)  # Opcional, cuando el pedido está pagado/convertido en venta
    total = db.Column(db.Float, nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('pedidos', lazy=True))
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'))
