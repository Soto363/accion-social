from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Inclusion(db.Model):
    __tablename__ = 'inclusiones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    tiene_discapacidad = db.Column(db.String(5), nullable=False)
    incapacidad = db.Column(db.String(100), nullable=True)
    
    # Relaciones
    informacion_general = db.relationship('InformacionGeneral', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    contacto = db.relationship('Contacto', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    familia_red_apoyo = db.relationship('FamiliaRedApoyo', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    educacion_ocupacion = db.relationship('EducacionOcupacion', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    salud = db.relationship('Salud', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    seguridad_social = db.relationship('SeguridadSocial', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    datos_socioeconomicos = db.relationship('DatosSocioeconomicos', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    vivienda = db.relationship('Vivienda', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    actividades = db.relationship('Actividades', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    unidad_victimas = db.relationship('UnidadVictimas', backref='inclusion', uselist=False, cascade='all, delete-orphan')
    observaciones = db.relationship('Observaciones', backref='inclusion', uselist=False, cascade='all, delete-orphan')

class InformacionGeneral(db.Model):
    __tablename__ = 'informacion_general'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    fecha_aplicacion = db.Column(db.Date)
    tipo_identificacion = db.Column(db.String(30))
    sexo = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    zona_residencia = db.Column(db.String(10))
    barrio_vereda = db.Column(db.String(100))
    direccion_residencia = db.Column(db.String(150))

class Contacto(db.Model):
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    numero_contacto = db.Column(db.String(30))
    estado_civil = db.Column(db.String(20))

class FamiliaRedApoyo(db.Model):
    __tablename__ = 'familia_red_apoyo'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    vive_con = db.Column(db.String(50))

class EducacionOcupacion(db.Model):
    __tablename__ = 'educacion_ocupacion'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    ocupacion_actual = db.Column(db.String(50))
    nivel_escolaridad = db.Column(db.String(50))
    sabe_leer_escribir = db.Column(db.Boolean)
    educacion_informal = db.Column(db.Boolean)
    tipo_educacion_informal = db.Column(db.String(100))

class Salud(db.Model):
    __tablename__ = 'salud'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    enfermedad_fisica_mental = db.Column(db.Boolean)
    descripcion_enfermedad = db.Column(db.String(150))
    tiempo_con_enfermedad = db.Column(db.String(30))
    recibe_tratamiento = db.Column(db.Boolean)
    tratamiento = db.Column(db.String(150))
    frecuencia_medico = db.Column(db.String(50))
    tipo_discapacidad = db.Column(db.String(100))
    certificado_discapacidad = db.Column(db.Boolean)
    controles_periodicos = db.Column(db.Boolean)

class SeguridadSocial(db.Model):
    __tablename__ = 'seguridad_social'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    afiliado_salud = db.Column(db.Boolean)
    regimen_salud = db.Column(db.String(50))
    eps = db.Column(db.String(50))

class DatosSocioeconomicos(db.Model):
    __tablename__ = 'datos_socioeconomicos'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    registrado_sisben = db.Column(db.Boolean)
    grupo_sisben = db.Column(db.String(10))
    pertenece_cabildo = db.Column(db.Boolean)
    nombre_cabildo = db.Column(db.String(100))
    proveedor_economico = db.Column(db.String(50))
    tipo_pension = db.Column(db.String(100))
    tipo_subsidio = db.Column(db.String(100))
    otros_ingresos = db.Column(db.String(150))
    quien_administra_ingresos = db.Column(db.String(100))
    prioridades_ingresos = db.Column(db.Text)

class Vivienda(db.Model):
    __tablename__ = 'vivienda'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    tipo_vivienda = db.Column(db.String(50))
    estado_vivienda = db.Column(db.String(20))
    vive_hacinamiento = db.Column(db.Boolean)
    numero_banos = db.Column(db.Integer)
    servicios = db.Column(db.Text)

class Actividades(db.Model):
    __tablename__ = 'actividades'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    participa_actividades = db.Column(db.Boolean)
    tipo_actividades = db.Column(db.String(150))
    tiempo_libre = db.Column(db.Text)
    participa_centro_vida = db.Column(db.Boolean)
    cual_centro = db.Column(db.String(100))

class UnidadVictimas(db.Model):
    __tablename__ = 'unidad_victimas'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    es_victima = db.Column(db.Boolean)
    tiene_certificado = db.Column(db.Boolean)

class Observaciones(db.Model):
    __tablename__ = 'observaciones'
    id = db.Column(db.Integer, primary_key=True)
    inclusion_id = db.Column(db.Integer, db.ForeignKey('inclusiones.id'))
    observaciones = db.Column(db.Text)
    usuario = db.Column(db.String(100))
    familiar_usuario = db.Column(db.String(100))
    responsable_ficha = db.Column(db.String(100))
