from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Nuevos modelos
class Departamento(db.Model):
    __tablename__ = 'departamento'
    id_departamento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(10), unique=True)
    ciudades = db.relationship('Ciudad', backref='departamento', lazy=True)

class Ciudad(db.Model):
    __tablename__ = 'ciudad'
    id_ciudad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(10), unique=True)
    id_departamento = db.Column(db.Integer, db.ForeignKey('departamento.id_departamento'), nullable=False)
    clientes = db.relationship('Cliente', backref='ciudad', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    id_ciudad = db.Column(db.Integer, db.ForeignKey('ciudad.id_ciudad'))
    ordenes_trabajo = db.relationship('OrdenTrabajo', backref='cliente', lazy=True)
    facturas = db.relationship('Factura', backref='cliente', lazy=True)

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id_administrador = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    __tablename__ = 'producto'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Numeric(10,2))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    ordenes_trabajo = db.relationship('OrdenTrabajo', backref='producto', lazy=True)
    ordenes_servicio = db.relationship('OrdenServicio', backref='producto', lazy=True)
    detalles_factura = db.relationship('DetalleFactura', backref='producto', lazy=True)

class EstadoOrdenTrabajo(db.Model):
    __tablename__ = 'estado_orden_trabajo'

    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(30), unique=True, nullable=False)
    ordenes_trabajo = db.relationship('OrdenTrabajo', backref='estado', lazy=True)

    @staticmethod
    def insert_estados_iniciales():
        estados = ['Recibido', 'En Proceso', 'En Revisión', 'Completado', 'Cancelado']
        for nombre in estados:
            if not EstadoOrdenTrabajo.query.filter_by(nombre_estado=nombre).first():
                estado = EstadoOrdenTrabajo(nombre_estado=nombre)
                db.session.add(estado)
        db.session.commit()

class EstadoOrdenServicio(db.Model):
    __tablename__ = 'estado_orden_servicio'

    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(30), unique=True, nullable=False)
    ordenes_servicio = db.relationship('OrdenServicio', backref='estado', lazy=True)

    @staticmethod
    def insert_estados_iniciales():
        estados = ['Pendiente', 'En Tránsito', 'En Taller Externo', 'Retornado', 'Entregado']
        for nombre in estados:
            if not EstadoOrdenServicio.query.filter_by(nombre_estado=nombre).first():
                estado = EstadoOrdenServicio(nombre_estado=nombre)
                db.session.add(estado)
        db.session.commit()

class EstadoFactura(db.Model):
    __tablename__ = 'estado_factura'
    id_estado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    facturas = db.relationship('Factura', backref='estado_factura', lazy=True)

class MetodoPago(db.Model):
    __tablename__ = 'metodo_pago'
    id_metodo_pago = db.Column(db.Integer, primary_key=True)
    tipo_pago = db.Column(db.String(50))
    facturas = db.relationship('Factura', backref='metodo_pago', lazy=True)

class HistorialEstado(db.Model):
    __tablename__ = 'historial_estado'

    id_historial = db.Column(db.Integer, primary_key=True)
    id_orden_trabajo = db.Column(db.Integer, db.ForeignKey('orden_trabajo.id_orden_trabajo'), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_orden_trabajo.id_estado'), nullable=False)
    fecha_cambio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_administrador = db.Column(db.Integer, db.ForeignKey('administrador.id_administrador'), nullable=False)
    observaciones = db.Column(db.Text)

    orden = db.relationship('OrdenTrabajo', backref='historial_estados')
    estado_info = db.relationship('EstadoOrdenTrabajo')
    administrador = db.relationship('Administrador')

class OrdenTrabajo(db.Model):
    __tablename__ = 'orden_trabajo'

    id_orden_trabajo = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_entrega_estimada = db.Column(db.DateTime)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_orden_trabajo.id_estado'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    observaciones = db.Column(db.Text)
    prioridad = db.Column(db.Integer, default=3)
    servicios = db.relationship('OrdenServicio', backref='orden_trabajo_rel', lazy=True)

    def cambiar_estado(self, nuevo_estado_id, admin_id, observaciones=None):
        self.id_estado = nuevo_estado_id
        historial = HistorialEstado(
            id_orden_trabajo=self.id_orden_trabajo,
            id_estado=nuevo_estado_id,
            id_administrador=admin_id,
            observaciones=observaciones
        )
        db.session.add(historial)
        db.session.commit()

class Transporte(db.Model):
    __tablename__ = 'transporte'

    id_transporte = db.Column(db.Integer, primary_key=True)
    fecha_envio = db.Column(db.DateTime)
    fecha_retorno = db.Column(db.DateTime)
    responsable_envio = db.Column(db.String(100))
    destino = db.Column(db.String(100))
    contacto_destino = db.Column(db.String(100))
    costo_transporte = db.Column(db.Numeric(10,2))
    ordenes_servicio = db.relationship('OrdenServicio', backref='transporte_rel', lazy=True)

class OrdenServicio(db.Model):
    __tablename__ = 'orden_servicio'

    id_orden_servicio = db.Column(db.Integer, primary_key=True)
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_envio_pasto = db.Column(db.DateTime)
    fecha_retorno_ipiales = db.Column(db.DateTime)
    fecha_entrega_cliente = db.Column(db.DateTime)
    descripcion_servicio = db.Column(db.Text)
    costo_servicio = db.Column(db.Numeric(10,2))
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_orden_servicio.id_estado'), nullable=False)
    id_orden_trabajo = db.Column(db.Integer, db.ForeignKey('orden_trabajo.id_orden_trabajo'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    id_transporte = db.Column(db.Integer, db.ForeignKey('transporte.id_transporte'))

class Factura(db.Model):
    __tablename__ = 'factura'

    id_factura = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.Date)
    fecha_remision = db.Column(db.DateTime)
    observacion = db.Column(db.String(200))
    abono = db.Column(db.Numeric(10,2), default=0)
    total_bruto = db.Column(db.Numeric(10,2), default=0)
    descuento = db.Column(db.Numeric(10,2), default=0)
    iva = db.Column(db.Numeric(10,2), default=0)
    total_a_pagar = db.Column(db.Numeric(10,2), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_factura.id_estado'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    id_administrador = db.Column(db.Integer, db.ForeignKey('administrador.id_administrador'), nullable=False)
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodo_pago.id_metodo_pago'))
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'

    id_detalle_factura = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_factura'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)

def inicializar_datos(app):
    with app.app_context():
        for nombre in ['Recibido', 'En Proceso', 'En Revisión', 'Completado', 'Cancelado']:
            if not EstadoOrdenTrabajo.query.filter_by(nombre_estado=nombre).first():
                db.session.add(EstadoOrdenTrabajo(nombre_estado=nombre))

        for nombre in ['Pendiente', 'En Tránsito', 'En Taller Externo', 'Retornado', 'Entregado']:
            if not EstadoOrdenServicio.query.filter_by(nombre_estado=nombre).first():
                db.session.add(EstadoOrdenServicio(nombre_estado=nombre))

        for nombre in ['Pendiente', 'Pagada', 'Anulada']:
            if not EstadoFactura.query.filter_by(nombre=nombre).first():
                db.session.add(EstadoFactura(nombre=nombre))

        for tipo in ['Efectivo', 'Transferencia', 'Tarjeta']:
            if not MetodoPago.query.filter_by(tipo_pago=tipo).first():
                db.session.add(MetodoPago(tipo_pago=tipo))

        if not Administrador.query.filter_by(usuario='admin').first():
            admin = Administrador(
                nombre='Administrador Principal',
                email='admin@empresa.com',
                usuario='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)

        if not Departamento.query.first():
            d1 = Departamento(nombre='Nariño', codigo='NAR')
            d2 = Departamento(nombre='Cundinamarca', codigo='CUN')
            db.session.add_all([d1, d2])
            db.session.flush()
            db.session.add_all([
                Ciudad(nombre='Ipiales', codigo='IPI', departamento=d1),
                Ciudad(nombre='Pasto', codigo='PAS', departamento=d1),
                Ciudad(nombre='Bogotá', codigo='BOG', departamento=d2)
            ])

        db.session.commit()


