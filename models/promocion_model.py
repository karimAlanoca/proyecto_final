from database import db

class Promocion(db.Model):
    __tablename__ = 'promociones'
    __table_args__ = {'extend_existing': True}  # Esto permite redefinirla sin error
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    descuento = db.Column(db.Float, nullable=False)  # porcentaje, ej. 15.0 para 15%
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)

    activa = db.Column(db.Boolean, nullable=False, default=True)  # <--- Aquí debe estar
