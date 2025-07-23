from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class FichaAdultoMayor(db.Model):
    __tablename__ = 'ficha_adulto_mayor'

    id = db.Column(db.Integer, primary_key=True)
    fecha_aplicacion = db.Column(db.Date, default=date.today)
    tipo_identificacion = db.Column(db.String(50), nullable=False)
   # otro_tipo_identificacion = db.Column(db.String(50), nullable=True)
    numero_identificacion = db.Column(db.String(50), unique=True, nullable=False)
    nombres_apellidos = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(20), nullable=True)
    sexo_otro = db.Column(db.String(50), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    zona_residencia = db.Column(db.String(10), nullable=True)
    barrio_vereda = db.Column(db.String(100), nullable=True)
    direccion_residencia = db.Column(db.Text, nullable=True)

    numero_contacto = db.Column(db.String(50), nullable=True)
    estado_civil = db.Column(db.String(30), nullable=True)
    convivencia = db.Column(db.String(30), nullable=True)
    convivencia_otro = db.Column(db.String(100), nullable=True)

    ocupacion = db.Column(db.String(50), nullable=True)
    escolaridad = db.Column(db.String(50), nullable=True)
    sabe_leer_escribir = db.Column(db.Boolean, nullable=True)
    educacion_informal = db.Column(db.Boolean, nullable=True)
    educacion_informal_cual = db.Column(db.String(100), nullable=True)

    enfermedad = db.Column(db.Boolean, nullable=True)
    enfermedad_cual = db.Column(db.String(100), nullable=True)
    tiempo_enfermedad = db.Column(db.String(50), nullable=True)
    tratamiento = db.Column(db.Boolean, nullable=True)
    tratamiento_cual = db.Column(db.String(100), nullable=True)
    frecuencia_medico = db.Column(db.String(50), nullable=True)

    discapacidad = db.Column(db.Boolean, nullable=True)
    tipo_discapacidad = db.Column(db.String(100), nullable=True)
    certificado_discapacidad = db.Column(db.Boolean, nullable=True)
    controles_periodicos = db.Column(db.Boolean, nullable=True)

    afiliado_salud = db.Column(db.Boolean, nullable=True)
    regimen_salud = db.Column(db.String(50), nullable=True)
    eps = db.Column(db.String(50), nullable=True)
    eps_otro = db.Column(db.String(50), nullable=True)

    registrado_sisben = db.Column(db.String(30), nullable=True)
    grupo_sisben = db.Column(db.String(10), nullable=True)
    pertenece_cabildo = db.Column(db.String(30), nullable=True)
    nombre_cabildo = db.Column(db.String(100), nullable=True)

    proveedor_economico = db.Column(db.String(50), nullable=True)
    pension = db.Column(db.String(50), nullable=True)
    pension_otro = db.Column(db.String(100), nullable=True)
    subsidio = db.Column(db.String(50), nullable=True)
    subsidio_otro = db.Column(db.String(100), nullable=True)
    otro_ingreso = db.Column(db.String(50), nullable=True)
    otro_ingreso_otro = db.Column(db.String(100), nullable=True)
    administra_ingresos = db.Column(db.String(50), nullable=True)
    destino_ingresos = db.Column(db.Text, nullable=True)

    tipo_vivienda = db.Column(db.String(50), nullable=True)
    estado_vivienda = db.Column(db.String(50), nullable=True)
    hacinamiento = db.Column(db.Boolean, nullable=True)
    numero_banos = db.Column(db.Integer, nullable=True)
    servicios = db.Column(db.Text, nullable=True)

    participa_actividades = db.Column(db.Boolean, nullable=True)
    actividades_cuales = db.Column(db.String(100), nullable=True)
    uso_tiempo_libre = db.Column(db.String(100), nullable=True)
    centro_vida = db.Column(db.Boolean, nullable=True)
    centro_vida_cual = db.Column(db.String(100), nullable=True)

    victima_conflicto = db.Column(db.Boolean, nullable=True)
    certificado_victima = db.Column(db.Boolean, nullable=True)

    observaciones = db.Column(db.Text, nullable=True)
    familiar_usuario = db.Column(db.String(100), nullable=True)
    responsable_funcionario = db.Column(db.String(100), nullable=True)
