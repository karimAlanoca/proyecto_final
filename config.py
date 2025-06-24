import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-app'
    SECRET_ADMIN_KEY = os.environ.get('SECRET_ADMIN_KEY') or 'clave-admin-secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False