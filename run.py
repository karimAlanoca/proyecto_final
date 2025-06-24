from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from database import db, init_app
#from flask_migrate import Migrate


#migrate = Migrate( db)

# Solo importar Usuario para el login_manager
from models.usuario_model import Usuario

# Blueprints
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.cliente_controller import cliente_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa SQLAlchemy
    init_app(app)

    # Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(cliente_bp, url_prefix='/cliente')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)
