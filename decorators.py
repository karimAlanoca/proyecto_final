from flask import flash, redirect, url_for, request
from flask_login import current_user
from functools import wraps
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión como administrador', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.es_admin():
            flash('Acceso restringido a administradores', 'danger')
            return redirect(url_for('index'))
            
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin():
            flash('Acceso denegado', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function