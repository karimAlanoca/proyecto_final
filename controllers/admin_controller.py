from flask import Blueprint, render_template, abort,redirect, url_for, request, flash
from datetime import datetime
from werkzeug.security import generate_password_hash
from models.factura_model import Factura

from flask_login import current_user, login_required
from functools import wraps
from models.usuario_model import Usuario
from models.producto_model import Producto
from models.venta_model import Venta
from models.pedido_model import Pedido
from models.proveedor_model import Proveedor
from models.venta_model import Venta
from models.promocion_model import Promocion
from models.cliente_model import Cliente
from database import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates')

# Decorador personalizado para verificar admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin():
           return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# @admin_bp.route('/dashboard')
# @login_required
# @admin_required
# def dashboard():
#     return render_template('admin/dashboard.html')

# #crud de usuario
# @admin_bp.route('/usuarios')
# #@login_required
# @admin_required
# def usuarios():
#     from models.usuario_model import Usuario  # Import local para evitar circular imports
#     usuarios = Usuario.query.all()
#     return render_template('admin/usuarios.html', usuarios=usuarios)

# #crud productos
# @admin_bp.route('/productos')
# #@login_required
# @admin_required
# def productos():
#     from models.producto_model import Producto
#     productos = Producto.query.all()
#     return render_template('admin/productos.html', productos=productos)

# #crud ventas 
# @admin_bp.route('/ventas')
# #@login_required
# @admin_required
# def ventas():
#     from models.venta_model import Venta  # Asegúrate de crear este modelo
#     ventas = Venta.query.all()
#    # ventas = Venta.query.order_by(Venta.fecha.desc()).all()
#     return render_template('admin/ventas.html', ventas=ventas)

# @admin_bp.route('/pedidos')
# #@login_required
# @admin_required
# def pedidos():
#     from models.pedido_model import Pedido  # Asegúrate de crear este modelo
#     pedidos = Pedido.query.all()
#     #pedidos = Pedido.query.filter_by(estado='pendiente').all()
#     return render_template('admin/pedidos.html', pedidos=pedidos)

# @admin_bp.route('/proveedores')
# @admin_required
# def proveedores():
#     from models.proveedor_model import Proveedor
#     proveedores = Proveedor.query.all()
#     return render_template('admin/proveedores.html', proveedores=proveedores)

# @admin_bp.route('/promociones')
# @admin_required
# def promociones():
#     from models.promocion_model import Promocion
#     promociones = Promocion.query.all()
#     return render_template('admin/promociones.html', promociones=promociones)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/usuarios')
@login_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

# @admin_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
# def agregar_usuario():
#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         # obtén otros campos...
#         nuevo_usuario = Usuario(nombre=nombre)
#         db.session.add(nuevo_usuario)
#         db.session.commit()
#         return redirect(url_for('admin.usuarios'))
#     return render_template('admin/agregar_usuario.html')

@admin_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        # Crear usuario
        nuevo_usuario = Usuario(
            email=email,
            username=email,
            password=generate_password_hash(password),
            rol=rol
        )
        db.session.add(nuevo_usuario)
        db.session.flush()  # obtener ID

        # Si es cliente, crea también cliente
        if rol == 'cliente':
            nuevo_cliente = Cliente(
                usuario_id=nuevo_usuario.id,
                nombre=nombre,
                telefono=telefono,
                direccion=direccion,
                email=email,
                password=nuevo_usuario.password  # se guarda en ambos
            )
            db.session.add(nuevo_cliente)

        db.session.commit()
        #flash('Usuario registrado correctamente.', 'success')
        return redirect(url_for('admin.usuarios'))

    return render_template('admin/agregar_usuario.html')


@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'], endpoint='editar_usuario_cliente')
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    cliente = Cliente.query.filter_by(usuario_id=usuario.id).first()

    if request.method == 'POST':
        usuario.email = request.form['email']
        usuario.username = request.form['email']
        usuario.rol = request.form['rol']
        password = request.form['password']
        if password:
            usuario.password = generate_password_hash(password)

        if usuario.rol == 'cliente':
            if not cliente:
                cliente = Cliente(usuario_id=usuario.id)
                db.session.add(cliente)
            cliente.nombre = request.form['nombre']
            cliente.telefono = request.form['telefono']
            cliente.direccion = request.form['direccion']
            cliente.email = usuario.email
            cliente.password = usuario.password  # O deja en blanco si no cambia
        else:
            if cliente:
                db.session.delete(cliente)

        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('admin.usuarios'))

    return render_template('admin/editar_usuario.html', usuario=usuario, cliente=cliente)



@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
     usuario = Usuario.query.get_or_404(id)
     if request.method == 'POST':
         usuario.nombre = request.form['nombre']
         usuario.email = request.form['email']
         db.session.commit()
         flash('Usuario actualizado')
         return redirect(url_for('admin.usuarios'))
     return render_template('admin/editar_usuario.html', usuario=usuario)

@admin_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/productos')
@login_required
def productos():
    productos = Producto.query.all()
    return render_template('admin/productos.html', productos=productos)

@admin_bp.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    if request.method == 'POST':
        nuevo = Producto(nombre=request.form['nombre'], precio=request.form['precio'],stock =request.form['stock'])
        db.session.add(nuevo)
        db.session.commit()
        flash('Producto agregado')
        return redirect(url_for('admin.productos'))
    return render_template('admin/agregar_producto.html')

@admin_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.stock = request.form['stock']
        
        db.session.commit()
        flash('Producto actualizado')
        return redirect(url_for('admin.productos'))
    return render_template('admin/editar_producto.html', producto=producto)

@admin_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado')
    return redirect(url_for('admin.productos'))

@admin_bp.route('/ventas')
@login_required
def ventas():
    ventas = Venta.query.all()
    return render_template('admin/ventas.html', ventas=ventas)

@admin_bp.route('/ventas/<int:id>', endpoint='ver_venta')
@login_required
def ver_venta(id):
    venta = Venta.query.get_or_404(id)
    return render_template('admin/ver_venta.html', venta=venta)

@admin_bp.route('/ventas/eliminar/<int:id>', methods=['POST', 'GET'], endpoint='eliminar_venta')
@login_required
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    flash('Venta eliminada exitosamente', 'success')
    return redirect(url_for('admin.ventas'))

@admin_bp.route('/ventas/<int:id>/factura', endpoint='ver_factura')
@login_required
def ver_factura(id):
    factura = Factura.query.filter_by(venta_id=id).first_or_404()
    return render_template('admin/ver_factura.html', factura=factura)



@admin_bp.route('/pedidos')
@login_required
def pedidos():
    pedidos = Pedido.query.all()
    return render_template('admin/pedidos.html', pedidos=pedidos)

@admin_bp.route('/proveedores')
@login_required
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('admin/proveedores.html', proveedores=proveedores)


# Listar proveedores
# @admin_bp.route('/proveedores')
# @login_required
# def proveedores_lista():
#     proveedores = Proveedor.query.all()
#     return render_template('admin/proveedores.html', proveedores=proveedores)

@admin_bp.route('/proveedores/nuevo')
@login_required
def nuevo_proveedor():
    return render_template('admin/nuevo_proveedor.html')


# Agregar proveedor
@admin_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def proveedores_nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        nuevo = Proveedor(nombre=nombre, telefono=telefono, email=email, direccion=direccion)
        db.session.add(nuevo)
        db.session.commit()
        flash('Proveedor creado correctamente', 'success')
        return redirect(url_for('admin.proveedores'))
    return render_template('admin/nuevo_proveedor.html')

@admin_bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.telefono = request.form['telefono']
        proveedor.correo = request.form['correo']
        proveedor.direccion = request.form['direccion']
        
        db.session.commit()
        flash('Proveedor actualizado exitosamente.', 'success')
        return redirect(url_for('admin.proveedores'))

    return render_template('admin/editar_proveedor.html', proveedor=proveedor)

@admin_bp.route('/proveedores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado exitosamente.', 'success')
    return redirect(url_for('admin.proveedores'))




# Similar para promociones:

@admin_bp.route('/promociones')
@login_required
def promociones():
    promociones = Promocion.query.all()
    return render_template('admin/promociones.html', promociones=promociones)

@admin_bp.route('/promociones/nueva', methods=['GET', 'POST'])
@login_required
def nueva_promocion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        descuento = float(request.form['descuento'])
        fecha_inicio = request.form['fecha_inicio']  # debes parsear datetime
        fecha_fin = request.form['fecha_fin']        # igual aquí
        activa = 'activa' in request.form
        nueva = Promocion(
            nombre=nombre,
            descripcion=descripcion,
            descuento=descuento,
            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d'),
            fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d'),
            activa=activa
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Promoción creada correctamente', 'success')
        return redirect(url_for('admin.promociones'))
    return render_template('admin/nueva_promocion.html')

@admin_bp.route('/promociones/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_promocion(id):
    promocion = Promocion.query.get_or_404(id)

    if request.method == 'POST':
        promocion.nombre = request.form['nombre']
        promocion.descripcion = request.form['descripcion']
        promocion.descuento = float(request.form['descuento'])
        promocion.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        promocion.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
        promocion.activa = 'activa' in request.form

        db.session.commit()
        flash('Promoción actualizada correctamente', 'success')
        return redirect(url_for('admin.promociones'))

    return render_template('admin/editar_promociones.html', promocion=promocion)

@admin_bp.route('/promociones/eliminar/<int:id>', methods=['POST', 'GET'])
@login_required
def eliminar_promocion(id):
    promocion = Promocion.query.get_or_404(id)
    db.session.delete(promocion)
    db.session.commit()
    flash('Promoción eliminada correctamente', 'success')
    return redirect(url_for('admin.promociones'))
