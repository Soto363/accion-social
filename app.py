from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Ciudad, Cliente, Producto, Categoria, Administrador, OrdenTrabajo, EstadoOrdenTrabajo, OrdenServicio, HistorialEstado
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from models import inicializar_datos

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configuración de seguridad adicional
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Por favor inicie sesión para acceder a esta página', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/index')  
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario').strip()
        contrasena = request.form.get('contrasena').strip()
        
        if not usuario or not contrasena:
            flash('Por favor ingrese usuario y contraseña', 'danger')
            return redirect(url_for('login'))
        
        admin = Administrador.query.filter_by(usuario=usuario).first()
        
        if not admin or not check_password_hash(admin.contrasena, contrasena):
            flash('Credenciales incorrectas', 'danger')
            return redirect(url_for('login'))
        
        session['admin_id'] = admin.id_administrador
        session['admin_nombre'] = admin.nombre
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Ha cerrado sesión correctamente', 'info')
    return redirect(url_for('login'))

# Rutas para Clientes

@app.route('/clientes')
@login_required
def clientes():
    busqueda = request.args.get('busqueda', '').strip()
    pagina = request.args.get('pagina', 1, type=int)
    
    query = Cliente.query
    
    if busqueda:
        query = query.filter(Cliente.nombre.ilike(f'%{busqueda}%')) | \
                query.filter(Cliente.cedula.ilike(f'%{busqueda}%'))
    
    clientes_paginados = query.paginate(page=pagina, per_page=10, error_out=False)
    
    return render_template('clientes/index.html', 
                         clientes=clientes_paginados,
                         busqueda=busqueda)

@app.route('/clientes/crear', methods=['GET', 'POST'])
@login_required
def crear_cliente():
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    if request.method == 'POST':
        try:
            nuevo = Cliente(
                cedula=request.form['cedula'].strip(),
                nombre=request.form['nombre'].strip(),
                telefono=request.form['telefono'].strip(),
                email=request.form['email'].strip(),
                direccion=request.form['direccion'].strip(),
                id_ciudad=int(request.form['id_ciudad'])  # nueva línea
            )
            db.session.add(nuevo)
            db.session.commit()
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cliente: {str(e)}', 'danger')
    
    return render_template('clientes/crear.html', ciudades=ciudades)

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    
    if request.method == 'POST':
        try:
            cliente.cedula = request.form['cedula'].strip()
            cliente.nombre = request.form['nombre'].strip()
            cliente.telefono = request.form['telefono'].strip()
            cliente.email = request.form['email'].strip()
            cliente.direccion = request.form['direccion'].strip()
            cliente.id_ciudad = int(request.form['id_ciudad'])  # nueva línea
            
            db.session.commit()
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}', 'danger')
    
    return render_template('clientes/editar.html', cliente=cliente, ciudades=ciudades)


@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar el cliente: {str(e)}', 'danger')
    
    return redirect(url_for('clientes'))

# Rutas para Productos 
@app.route('/productos')
@login_required
def productos():
    busqueda = request.args.get('busqueda', '').strip()
    pagina = request.args.get('pagina', 1, type=int)
    
    query = Producto.query
    
    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))
    
    productos_paginados = query.paginate(page=pagina, per_page=10, error_out=False)
    
    return render_template('productos/index.html', 
                         productos=productos_paginados,
                         busqueda=busqueda)

@app.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        try:
            nuevo = Producto(
                nombre=request.form['nombre'].strip(),
                descripcion=request.form['descripcion'].strip(),
                precio=float(request.form['precio']),
                id_categoria=int(request.form['id_categoria'])
            )
            db.session.add(nuevo)
            db.session.commit()
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('productos'))
        except ValueError:
            flash('Error en los datos ingresados. Verifique el precio y categoría', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear producto: {str(e)}', 'danger')
    
    return render_template('productos/crear.html', categorias=categorias)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre'].strip()
            producto.descripcion = request.form['descripcion'].strip()
            producto.precio = float(request.form['precio'])
            producto.id_categoria = int(request.form['id_categoria'])
            
            db.session.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos'))
        except ValueError:
            flash('Error en los datos ingresados', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar producto: {str(e)}', 'danger')
    
    return render_template('productos/editar.html', 
                         producto=producto,
                         categorias=categorias)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    try:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar el producto: {str(e)}', 'danger')
    
    return redirect(url_for('productos'))

# Rutas para Categorías
@app.route('/categorias')
@login_required
def categorias():
    categorias = Categoria.query.all()
    return render_template('categorias/index.html', categorias=categorias)

@app.route('/categorias/crear', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    if request.method == 'POST':
        nueva = Categoria(nombre=request.form['nombre'])
        db.session.add(nueva)
        db.session.commit()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('categorias'))
    return render_template('categorias/crear.html')

# Rutas para Órdenes de Trabajo
@app.route('/ordenes-trabajo')
@login_required
def ordenes_trabajo():
    # Obtener parámetros de búsqueda y paginación
    estado = request.args.get('estado', '')
    cliente_id = request.args.get('cliente_id', '')
    pagina = request.args.get('pagina', 1, type=int)
    
    # Construir consulta
    query = OrdenTrabajo.query
    
    if estado:
        query = query.join(EstadoOrdenTrabajo).filter(EstadoOrdenTrabajo.nombre_estado == estado)
    if cliente_id:
        query = query.filter(OrdenTrabajo.id_cliente == cliente_id)
    
    # Ordenar por fecha de ingreso descendente
    query = query.order_by(OrdenTrabajo.fecha_ingreso.desc())
    
    # Paginación
    ordenes_paginadas = query.paginate(page=pagina, per_page=10, error_out=False)
    
    # Obtener datos para filtros
    estados = EstadoOrdenTrabajo.query.all()
    clientes = Cliente.query.all()
    
    return render_template('ordenes_trabajo/index.html',
                         ordenes=ordenes_paginadas,
                         estados=estados,
                         clientes=clientes,
                         filtros={'estado': estado, 'cliente_id': cliente_id})

@app.route('/ordenes-trabajo/crear', methods=['GET', 'POST'])
@login_required
def crear_orden_trabajo():
    if request.method == 'POST':
        try:
            nueva_orden = OrdenTrabajo(
                fecha_ingreso=datetime.now(),
                fecha_entrega_estimada=datetime.strptime(request.form['fecha_entrega'], '%Y-%m-%d'),
                id_estado=1,  # Estado inicial (ej: "Recibido")
                id_cliente=int(request.form['cliente']),
                id_producto=int(request.form['producto']),
                observaciones=request.form['observaciones'].strip()
            )
            
            db.session.add(nueva_orden)
            db.session.commit()
            
            flash('Orden de trabajo creada exitosamente', 'success')
            return redirect(url_for('detalle_orden_trabajo', id=nueva_orden.id_orden_trabajo))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear orden: {str(e)}', 'danger')
    
    # Datos para formulario
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    
    return render_template('ordenes_trabajo/crear.html',
                         clientes=clientes,
                         productos=productos)

@app.route('/ordenes-trabajo/<int:id>')
@login_required
def detalle_orden_trabajo(id):
    orden = OrdenTrabajo.query.get_or_404(id)
    estados = EstadoOrdenTrabajo.query.all()
    return render_template('ordenes_trabajo/detalle.html',
                         orden=orden,
                         estados=estados)

@app.route('/ordenes-trabajo/<int:id>/actualizar-estado', methods=['POST'])
@login_required
def actualizar_estado_orden(id):
    orden = OrdenTrabajo.query.get_or_404(id)
    
    try:
        nuevo_estado = int(request.form['estado'])
        orden.id_estado = nuevo_estado
        
        # Registrar cambio de estado
        historial = HistorialEstado(
            id_orden_trabajo=orden.id_orden_trabajo,
            id_estado=nuevo_estado,
            fecha_cambio=datetime.now(),
            id_administrador=session['admin_id']
        )
        
        db.session.add(historial)
        db.session.commit()
        
        flash('Estado actualizado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar estado: {str(e)}', 'danger')
    
    return redirect(url_for('detalle_orden_trabajo', id=id))

@app.route('/ordenes-trabajo/<int:id>/agregar-servicio', methods=['POST'])
@login_required
def agregar_servicio_orden(id):
    orden = OrdenTrabajo.query.get_or_404(id)
    
    try:
        nuevo_servicio = OrdenServicio(
            id_orden_trabajo=orden.id_orden_trabajo,
            id_producto=orden.id_producto,
            id_estado=1,  # Estado inicial para servicio
            fecha_recepcion=datetime.now(),
            descripcion_servicio=request.form['descripcion'].strip()
        )
        
        db.session.add(nuevo_servicio)
        db.session.commit()
        
        flash('Servicio agregado a la orden', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar servicio: {str(e)}', 'danger')
    
    return redirect(url_for('detalle_orden_trabajo', id=id))

    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from models import inicializar_datos
        inicializar_datos(app)  # Pasa la app como parámetro
    app.run(debug=True)
