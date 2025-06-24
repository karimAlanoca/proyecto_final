from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from models.usuario_model import Usuario
from models.cliente_model import Cliente

from forms import LoginForm, RegistrationForm
from database import db

CODIGO_ADMIN = "22"
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Decorador para requerir rol de admin
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('Acceso restringido a administradores', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def redirect_based_on_role():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.rol == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('cliente.catalogo'))

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
    
#     if form.validate_on_submit():
#         try:
#             # Verificar si el usuario ya existe
#             if Usuario.query.filter((Usuario.email == form.email.data) | 
#                                   (Usuario.username == form.username.data)).first():
#                 flash('El nombre de usuario o email ya están registrados', 'danger')
#                 return redirect(url_for('auth.register'))
            
#             # Validar clave de admin si corresponde
#             if form.role.data == 'admin' and form.admin_key.data != '22':
#                 flash('Clave de administrador incorrecta', 'danger')
#                 return render_template('auth/register.html', form=form)
            
#             # Crear nuevo usuario
#             nuevo_usuario = Usuario(
#                 username=form.username.data,
#                 email=form.email.data,
#                 password=generate_password_hash(form.password.data),
#                 rol=form.role.data  # 'admin' o 'cliente'
#             )
            
#             db.session.add(nuevo_usuario)
#             db.session.flush()
#             #db.session.commit()

#              # Si es cliente, crear registro en tabla clientes
#             if form.rol.data == 'cliente':
#                 cliente = Cliente(

#                     nombre=form.nombre['nombre'],
#                     telefono = form.telefono['telefono'],
#                     email = form.email['email'] ,
#                     password = form.password['telefono'],
#                     direccion = form.direccion['direccion'],
#                     usuario=nuevo_usuario  # Relación directa

#                 )
#                 db.session.add(cliente)
#             db.session.commit()
            
#             flash('Registro exitoso! Por favor inicia sesión', 'success')
#             return redirect(url_for('auth.login'))
            
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error al registrar el usuario: {str(e)}', 'danger')
    
#     return render_template('auth/register.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        username = email  # o lo puedes tomar de otro campo

        # Verifica si ya existe el email o el username
        usuario_existente = Usuario.query.filter(
            (Usuario.email == email) | (Usuario.username == username)
        ).first()

        if usuario_existente:
            flash('El correo o nombre de usuario ya están registrados.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            nuevo_usuario = Usuario(
                username=username,
                email=email,
                password=generate_password_hash(password),
                rol=rol
            )
            db.session.add(nuevo_usuario)
            db.session.flush()  # Aquí es seguro

            if rol == 'cliente':
                cliente = Cliente(
                    nombre=request.form['nombre'],
                    telefono=request.form['telefono'],
                    email=email,
                    password=generate_password_hash(password),
                    direccion=request.form['direccion'],
                    usuario_id=nuevo_usuario.id  # asignar el FK al usuario creado
                )
                db.session.add(cliente)
                flash('Cliente registrado exitosamente.', 'success')
            else:
                # Validar código admin
                if request.form.get('codigo_admin') != '22':
                    flash('Código de administrador incorrecto.', 'danger')
                    db.session.rollback()
                    return redirect(url_for('auth.register'))
                flash('Administrador registrado exitosamente.', 'success')

            db.session.commit()
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         usuario = Usuario.query.filter_by(email=request.form['email']).first()
#         if usuario and check_password_hash(usuario.password, request.form['password']):
#             login_user(usuario)
            
#             # Redirigir según rol
#             if usuario.es_admin():
#                 return redirect(url_for('admin.dashboard'))
#             else:
#                 return redirect(url_for('cliente.productos'))
    
#     return render_template('auth/login.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            if usuario.es_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('cliente.productos'))
        else:
            flash('Credenciales inválidas', 'danger')
          

    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout_v2():
    logout_user()
    return redirect(url_for('index'))

def redirect_based_on_role():
    if current_user.es_admin():
        return redirect(url_for('admin.dashboard'))
    else:
        return redirect(url_for('cliente.catalogo'))
    
