from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    
    # Importar modelos después de inicializar db
    with app.app_context():
        from models.usuario_model import Usuario
        from models.cliente_model import Cliente
        
        try:
            db.create_all()
            print("✅ Base de datos creada correctamente en:", app.config['SQLALCHEMY_DATABASE_URI'])
        except Exception as e:
            print("❌ Error al crear la base de datos:", str(e))
            raise

    