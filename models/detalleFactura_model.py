from database import db

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto', backref='detalles_factura')
