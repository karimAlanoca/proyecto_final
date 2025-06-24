from flask import Blueprint, render_template
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
#from models import Producto, Carrito, db
from models.producto_model import Producto
from models.carrito_model import Carrito
from models.venta_model import Venta
from models.pago_model import Pago
from datetime import datetime

from models.factura_model import Factura
from models.detalleFactura_model import DetalleFactura

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
print("ReportLab funciona!")

# def crear_pdf(nombre_archivo):
#     c = canvas.Canvas(nombre_archivo, pagesize=letter)
#     ancho, alto = letter
#     c.drawString(100, alto - 100, "Hola, este es un PDF generado con ReportLab")
#     c.save()

# crear_pdf("prueba.pdf")


from io import BytesIO
from flask import send_file
from datetime import datetime

hoy = datetime.now().date()


from database import db

from models.promocion_model import Promocion

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

# @cliente_bp.route('/productos')
# def productos():
#     productos = Producto.query.all()
#     return render_template('cliente/productos.html', productos=productos, promociones=promociones) 

@cliente_bp.route('/productos')
def productos():
    productos = Producto.query.all()
    promociones = Promocion.query.filter(
        Promocion.activa == True,
        Promocion.fecha_inicio <= hoy,
        Promocion.fecha_fin >= hoy
    ).all()
    return render_template('cliente/productos.html', productos=productos, promociones=promociones)


@cliente_bp.route('/catalogo')
@login_required
def catalogo():
    from models.producto_model import Producto
    productos = Producto.query.filter_by(disponible=True).all()
    return render_template('cliente/catalogo.html', productos=productos)

# @cliente_bp.route('/promociones')
# @login_required
# def promociones():
#     from models.promocion_model import Promocion
#     promociones = Promocion.query.filter_by(activa=True).all()
#     return render_template('cliente/promociones.html', promociones=promociones)

@cliente_bp.route('/promociones')
@login_required
def promociones():
    promociones_activas = Promocion.query.filter_by(activa=True).all()
    return render_template('cliente/promociones.html', promociones=promociones_activas)

# @cliente_bp.route('/carrito')
# @login_required
# def carrito():
#     items = Carrito.query.filter_by(usuario_id=current_user.id).all()
#     return render_template('cliente/carrito.html', items=items)
#     #return render_template('cliente/carrito.html')

@cliente_bp.route('/carrito')
@login_required
def carrito():
    items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    total = sum(item.cantidad * item.producto.precio for item in items)
    return render_template('cliente/carrito.html', items=items, total=total)


# @cliente_bp.route('/agregar_al_carrito/<int:producto_id>', methods=['POST'])
# def agregar_al_carrito(producto_id):
#     nuevo_item = Carrito(producto_id=producto_id, usuario_id=current_user.id)
#     db.session.add(nuevo_item)
#     db.session.commit()
#     flash("Producto añadido al carrito", "success")
#     return redirect(url_for('cliente.productos'))

@cliente_bp.route('/agregar_al_carrito/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    item_existente = Carrito.query.filter_by(usuario_id=current_user.id, producto_id=producto_id).first()
    if item_existente:
        item_existente.cantidad += 1
    else:
        nuevo_item = Carrito(producto_id=producto_id, usuario_id=current_user.id, cantidad=1)
        db.session.add(nuevo_item)
    db.session.commit()
    flash("Producto añadido al carrito", "success")
    return redirect(url_for('cliente.carrito'))

# @cliente_bp.route('/pagar', methods=['POST'])
# @login_required
# def pagar():
#     items = Carrito.query.filter_by(usuario_id=current_user.id).all()
#     if not items:
#         flash("Tu carrito está vacío.", "warning")
#         return redirect(url_for('cliente.productos'))

#     total = sum(item.producto.precio * item.cantidad for item in items)

#     nueva_venta = Venta(usuario_id=current_user.id, total=total)
#     db.session.add(nueva_venta)
#     db.session.flush()

#     nuevo_pago = Pago(venta_id=nueva_venta.id, metodo='Tarjeta')
#     db.session.add(nuevo_pago)

#     Carrito.query.filter_by(usuario_id=current_user.id).delete()
#     db.session.commit()

#     flash("Compra realizada con éxito", "success")
#     return redirect(url_for('cliente.productos'))




# @cliente_bp.route('/pagar', methods=['POST'])
# @login_required
# def pagar():
#     # Obtener productos del carrito del usuario
#     carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()

#     if not carrito_items:
#         flash('Tu carrito está vacío.', 'warning')
#         return redirect(url_for('cliente.ver_carrito'))

#     # Calcular total
#     total = sum(item.producto.precio * item.cantidad for item in carrito_items)

#     # Crear nueva venta
#     nueva_venta = Venta(usuario_id=current_user.id, total=total)
#     db.session.add(nueva_venta)
#     db.session.flush()  # asegura que nueva_venta.id esté disponible

#     # Crear pago
#     pago = Pago(venta_id=nueva_venta.id, monto=total, metodo='Tarjeta')
#     db.session.add(pago)

#     # Limpiar carrito
#     Carrito.query.filter_by(usuario_id=current_user.id).delete()

#     db.session.commit()
#     flash('Compra realizada con éxito.', 'success')
#     return redirect(url_for('cliente.productos'))

#-----------------------------------



@cliente_bp.route('/pagar', methods=['POST'])
@login_required
def pagar():
    carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()

    if not carrito_items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cliente.ver_carrito'))

    total = sum(item.producto.precio * item.cantidad for item in carrito_items)

    # Crear nueva venta
    nueva_venta = Venta(usuario_id=current_user.id, total=total, fecha=datetime.now())
    db.session.add(nueva_venta)
    db.session.flush()  # para tener nueva_venta.id

    # Crear pago
    pago = Pago(venta_id=nueva_venta.id, monto=total, metodo='Tarjeta', fecha=datetime.now())
    db.session.add(pago)

    # Crear factura
    factura = Factura(venta_id=nueva_venta.id, cliente_id=current_user.cliente.id, total=total, fecha=datetime.now())
    db.session.add(factura)
    db.session.flush()  # para factura.id

    # Crear detalles factura
    for item in carrito_items:
        detalle = DetalleFactura(
            factura_id=factura.id,
            producto_id=item.producto.id,
            cantidad=item.cantidad,
            subtotal=item.producto.precio * item.cantidad
        )
        db.session.add(detalle)
#---------------------------

#-------------------------
    # Limpiar carrito
    Carrito.query.filter_by(usuario_id=current_user.id).delete()

    db.session.commit()

    # Generar PDF de la factura
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setTitle(f"Factura_{factura.id}")

    y = 800
    p.drawString(50, y, f"Factura N°: {factura.id}")
    y -= 20
    p.drawString(50, y, f"Fecha: {factura.fecha.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    p.drawString(50, y, f"Cliente: {current_user.cliente.nombre}")
    y -= 40
    p.drawString(50, y, "Detalle:")
    y -= 20
    p.drawString(50, y, "Producto")
    p.drawString(250, y, "Cantidad")
    p.drawString(350, y, "Subtotal")
    y -= 20

    for detalle in factura.detalles:
        p.drawString(50, y, detalle.producto.nombre)
        p.drawString(250, y, str(detalle.cantidad))
        p.drawString(350, y, f"Bs. {detalle.subtotal:.2f}")
        y -= 20
        if y < 100:  # página nueva si baja mucho
            p.showPage()
            y = 800

    y -= 10
    p.drawString(50, y, f"Total: Bs. {factura.total:.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"factura_{factura.id}.pdf", mimetype='application/pdf')


#-------------------------

@cliente_bp.route('/pago')
@login_required
def pago():
    carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    if not carrito_items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cliente.ver_carrito'))

    total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    return render_template('cliente/pago.html', total=total)



# @cliente_bp.route('/pagar', methods=['POST'])
# @login_required
# def pagar():
#     carrito_items = Carrito.query.filter_by(usuario_id=current_user.id).all()
#     if not carrito_items:
#         flash('Tu carrito está vacío.', 'warning')
#         return redirect(url_for('cliente.ver_carrito'))

#     total = sum(item.producto.precio * item.cantidad for item in carrito_items)

#     nueva_venta = Venta(usuario_id=current_user.id, total=total)
#     db.session.add(nueva_venta)
#     db.session.flush()

#     pago = Pago(venta_id=nueva_venta.id, monto=total, metodo='Tarjeta')
#     db.session.add(pago)

#     for item in carrito_items:
#         detalle = DetalleFactura(
#             venta_id=nueva_venta.id,
#             producto_id=item.producto.id,
#             cantidad=item.cantidad,
#             precio_unitario=item.producto.precio
#         )
#         db.session.add(detalle)

#     Carrito.query.filter_by(usuario_id=current_user.id).delete()
#     db.session.commit()

#     flash('Compra realizada con éxito. Descarga tu factura.', 'success')
#     return redirect(url_for('cliente.factura_pdf', venta_id=nueva_venta.id))


@cliente_bp.route('/factura/<int:venta_id>')
@login_required
def factura_pdf(venta_id):
    venta = Venta.query.get_or_404(venta_id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Factura de Compra")
    p.setFont("Helvetica", 12)
    p.drawString(50, 730, f"ID Venta: {venta.id}")
    p.drawString(50, 715, f"Cliente: {current_user.username}")
    p.drawString(50, 700, f"Fecha: {venta.fecha.strftime('%d/%m/%Y')}")

    y = 670
    p.drawString(50, y, "Producto")
    p.drawString(250, y, "Cantidad")
    p.drawString(350, y, "Precio Unitario")
    p.drawString(470, y, "Subtotal")
    y -= 20

    for detalle in venta.detallefactura:
        p.drawString(50, y, detalle.producto.nombre)
        p.drawString(250, y, str(detalle.cantidad))
        p.drawString(350, y, f"Bs. {detalle.precio_unitario:.2f}")
        subtotal = detalle.cantidad * detalle.precio_unitario
        p.drawString(470, y, f"Bs. {subtotal:.2f}")
        y -= 20

    p.drawString(50, y - 10, f"Total: Bs. {venta.total:.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"factura_{venta.id}.pdf", mimetype='application/pdf')





@cliente_bp.route('/carrito/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_carrito(id):
    # Aquí elimina el producto del carrito de la base de datos, sesión, etc.
    # Ejemplo (ajusta según tu modelo y lógica):
    item = Carrito.query.filter_by(id=id, usuario_id=current_user.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Producto eliminado del carrito.', 'success')
    else:
        flash('Producto no encontrado en el carrito.', 'danger')

    return redirect(url_for('cliente.carrito'))



@cliente_bp.route('/carrito/actualizar/<int:id>', methods=['POST'])
@login_required
def actualizar_carrito(id):
    item = Carrito.query.get_or_404(id)
    nueva_cantidad = float(request.form['cantidad'])

    if nueva_cantidad <= 0:
        db.session.delete(item)
    else:
        item.cantidad = nueva_cantidad

    db.session.commit()
    flash('Carrito actualizado.', 'success')
    return redirect(url_for('cliente.carrito'))


