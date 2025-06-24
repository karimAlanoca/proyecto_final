from database import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    
    # ForeignKey para relacionar con Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True) 

    # Relación 1-1 con Usuario
    usuario = db.relationship('Usuario', back_populates='cliente')