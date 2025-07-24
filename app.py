from sqlalchemy.exc import IntegrityError 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, FichaAdultoMayor
from config import Config
from flask_migrate import Migrate
from datetime import datetime
import re
import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

# Configurar logging para debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return redirect(url_for('lista_adultos_mayores'))

# RUTAS ADULTO MAYOR
@app.route('/adulto-mayor/nuevo', methods=['GET', 'POST'])
def nuevo_adulto_mayor():
    if request.method == 'POST':
        # Debug: Imprimir todos los datos recibidos
        logger.debug("Datos recibidos del formulario:")
        for key, value in request.form.items():
            logger.debug(f"{key}: {value}")
        
        # Validaciones básicas
        errors = {}
        
        # Validar campos obligatorios
        campos_obligatorios = ['tipo_identificacion', 'numero_identificacion', 'nombres_apellidos']
        for campo in campos_obligatorios:
            if not request.form.get(campo):
                errors[campo] = f"El campo {campo} es obligatorio"
        
        # Validar número de identificación
        numero_id = request.form.get('numero_identificacion', '').strip()
        if numero_id and not re.match(r'^\d+$', numero_id):
            errors['numero_identificacion'] = "El número de identificación debe contener solo números"
        
        # Validar fecha de nacimiento
        fecha_nacimiento_str = request.form.get('fecha_nacimiento')
        fecha_nacimiento = None
        if fecha_nacimiento_str:
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
            except ValueError:
                errors['fecha_nacimiento'] = "Formato de fecha inválido"
        
        # Validar fecha de aplicación
        fecha_aplicacion_str = request.form.get('fecha_aplicacion')
        fecha_aplicacion = None
        if fecha_aplicacion_str:
            try:
                fecha_aplicacion = datetime.strptime(fecha_aplicacion_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_aplicacion = datetime.now().date()
        else:
            fecha_aplicacion = datetime.now().date()
        
        # Si hay errores de validación, devolverlos
        if errors:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "errors": errors})
            for error in errors.values():
                flash(error, 'danger')
            return render_template('adulto_mayor/nuevo.html')
        
        try:
            # Función helper para convertir checkbox values
            def get_boolean(field_name):
                value = request.form.get(field_name)
                return value == 'true' or value == 'on' or value == '1'
            
            # Función helper para obtener entero
            def get_int(field_name, default=None):
                value = request.form.get(field_name)
                if value and value.strip():
                    try:
                        return int(value)
                    except ValueError:
                        return default
                return default
            
            # Crear la ficha con todos los campos del modelo
            ficha = FichaAdultoMayor(
                fecha_aplicacion=fecha_aplicacion,
                tipo_identificacion=request.form.get('tipo_identificacion'),
                otro_tipo_identificacion=request.form.get('otro_tipo_identificacion') or None,
                numero_identificacion=numero_id,
                nombres_apellidos=request.form.get('nombres_apellidos').strip(),
                sexo=request.form.get('sexo') or None,
                sexo_otro=request.form.get('sexo_otro') or None,
                fecha_nacimiento=fecha_nacimiento,
                edad=get_int('edad'),
                zona_residencia=request.form.get('zona_residencia') or None,
                barrio_vereda=request.form.get('barrio_vereda') or None,
                direccion_residencia=request.form.get('direccion_residencia') or None,
                
                # Información de contacto
                numero_contacto=request.form.get('numero_contacto') or None,
                estado_civil=request.form.get('estado_civil') or None,
                convivencia=request.form.get('convivencia') or None,
                convivencia_otro=request.form.get('convivencia_otro') or None,
                
                # Información educativa y laboral
                ocupacion=request.form.get('ocupacion') or None,
                escolaridad=request.form.get('escolaridad') or None,
                sabe_leer_escribir=get_boolean('sabe_leer_escribir'),
                educacion_informal=get_boolean('educacion_informal'),
                educacion_informal_cual=request.form.get('educacion_informal_cual') or None,
                
                # Información de salud
                enfermedad=get_boolean('enfermedad'),
                enfermedad_cual=request.form.get('enfermedad_cual') or None,
                tiempo_enfermedad=request.form.get('tiempo_enfermedad') or None,
                tratamiento=get_boolean('tratamiento'),
                tratamiento_cual=request.form.get('tratamiento_cual') or None,
                frecuencia_medico=request.form.get('frecuencia_medico') or None,
                
                # Discapacidad
                discapacidad=get_boolean('discapacidad'),
                tipo_discapacidad=request.form.get('tipo_discapacidad') or None,
                certificado_discapacidad=get_boolean('certificado_discapacidad'),
                controles_periodicos=get_boolean('controles_periodicos'),
                
                # Afiliación a salud
                afiliado_salud=get_boolean('afiliado_salud'),
                regimen_salud=request.form.get('regimen_salud') or None,
                eps=request.form.get('eps') or None,
                eps_otro=request.form.get('eps_otro') or None,
                
                # SISBEN y cabildo
                registrado_sisben=request.form.get('registrado_sisben') or None,
                grupo_sisben=request.form.get('grupo_sisben') or None,
                pertenece_cabildo=request.form.get('pertenece_cabildo') or None,
                nombre_cabildo=request.form.get('nombre_cabildo') or None,
                
                # Información económica
                proveedor_economico=request.form.get('proveedor_economico') or None,
                pension=request.form.get('pension') or None,
                pension_otro=request.form.get('pension_otro') or None,
                subsidio=request.form.get('subsidio') or None,
                subsidio_otro=request.form.get('subsidio_otro') or None,
                otro_ingreso=request.form.get('otro_ingreso') or None,
                otro_ingreso_otro=request.form.get('otro_ingreso_otro') or None,
                administra_ingresos=request.form.get('administra_ingresos') or None,
                destino_ingresos=request.form.get('destino_ingresos') or None,
                
                # Información de vivienda
                tipo_vivienda=request.form.get('tipo_vivienda') or None,
                estado_vivienda=request.form.get('estado_vivienda') or None,
                hacinamiento=get_boolean('hacinamiento'),
                numero_banos=get_int('numero_banos', 0),
                servicios=request.form.get('servicios') or None,
                
                # Actividades y tiempo libre
                participa_actividades=get_boolean('participa_actividades'),
                actividades_cuales=request.form.get('actividades_cuales') or None,
                uso_tiempo_libre=request.form.get('uso_tiempo_libre') or None,
                centro_vida=get_boolean('centro_vida'),
                centro_vida_cual=request.form.get('centro_vida_cual') or None,
                
                # Víctimas del conflicto
                victima_conflicto=get_boolean('victima_conflicto'),
                certificado_victima=get_boolean('certificado_victima'),
                
                # Observaciones y responsables
                observaciones=request.form.get('observaciones') or None,
                familiar_usuario=request.form.get('familiar_usuario') or None,
                responsable_funcionario=request.form.get('responsable_funcionario') or None
            )

            logger.debug(f"Intentando guardar ficha para: {ficha.nombres_apellidos}")
            
            db.session.add(ficha)
            db.session.commit()
            
            logger.info(f"Ficha guardada exitosamente con ID: {ficha.id}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    "success": True, 
                    "message": "Ficha guardada exitosamente", 
                    "id": ficha.id,
                    "redirect": url_for('lista_adultos_mayores')
                })
            
            flash('Ficha del adulto mayor registrada exitosamente', 'success')
            return redirect(url_for('lista_adultos_mayores'))

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f'Error de integridad: {str(e)}')
            mensaje = 'El número de identificación ya está registrado.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "errors": {"numero_identificacion": mensaje}})
            flash(mensaje, 'danger')
            
        except ValueError as e:
            db.session.rollback()
            logger.error(f'Error de valor: {str(e)}')
            mensaje = 'Datos inválidos en el formulario.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "errors": {"general": mensaje}})
            flash(mensaje, 'danger')
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error inesperado al guardar ficha: {str(e)}', exc_info=True)
            mensaje = f'Error al guardar los datos: {str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "errors": {"general": mensaje}})
            flash(mensaje, 'danger')

    return render_template('adulto_mayor/nuevo.html')

@app.route('/adulto-mayor/editar/<int:id>', methods=['GET', 'POST'])
def editar_adulto_mayor(id):
    ficha = FichaAdultoMayor.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # Función helper para convertir checkbox values
            def get_boolean(field_name):
                value = request.form.get(field_name)
                return value == 'true' or value == 'on' or value == '1'
            
            def get_int(field_name, default=None):
                value = request.form.get(field_name)
                if value and value.strip():
                    try:
                        return int(value)
                    except ValueError:
                        return default
                return default

            # Actualizar todos los campos
            ficha.fecha_aplicacion = datetime.strptime(request.form.get('fecha_aplicacion'), '%Y-%m-%d').date()
            ficha.tipo_identificacion = request.form.get('tipo_identificacion')
            ficha.otro_tipo_identificacion = request.form.get('otro_tipo_identificacion')
            ficha.nombres_apellidos = request.form.get('nombres_apellidos')
            ficha.numero_identificacion = request.form.get('numero_identificacion')
            ficha.sexo = request.form.get('sexo')
            ficha.sexo_otro = request.form.get('sexo_otro')
            
            if request.form.get('fecha_nacimiento'):
                ficha.fecha_nacimiento = datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d').date()
            
            ficha.edad = get_int('edad')
            ficha.zona_residencia = request.form.get('zona_residencia')
            ficha.barrio_vereda = request.form.get('barrio_vereda')
            ficha.direccion_residencia = request.form.get('direccion_residencia')
            ficha.numero_contacto = request.form.get('numero_contacto')
            ficha.estado_civil = request.form.get('estado_civil')
            ficha.convivencia = request.form.get('convivencia')
            ficha.convivencia_otro = request.form.get('convivencia_otro')
            
            ficha.ocupacion = request.form.get('ocupacion')
            ficha.escolaridad = request.form.get('escolaridad')
            ficha.sabe_leer_escribir = get_boolean('sabe_leer_escribir')
            ficha.educacion_informal = get_boolean('educacion_informal')
            ficha.educacion_informal_cual = request.form.get('educacion_informal_cual')
            
            # Salud
            ficha.enfermedad = get_boolean('enfermedad')
            ficha.enfermedad_cual = request.form.get('enfermedad_cual')
            ficha.tiempo_enfermedad = request.form.get('tiempo_enfermedad')
            ficha.tratamiento = get_boolean('tratamiento')
            ficha.tratamiento_cual = request.form.get('tratamiento_cual')
            ficha.frecuencia_medico = request.form.get('frecuencia_medico')
            
            # Discapacidad
            ficha.discapacidad = get_boolean('discapacidad')
            ficha.tipo_discapacidad = request.form.get('tipo_discapacidad')
            ficha.certificado_discapacidad = get_boolean('certificado_discapacidad')
            ficha.controles_periodicos = get_boolean('controles_periodicos')
            
            # Salud
            ficha.afiliado_salud = get_boolean('afiliado_salud')
            ficha.regimen_salud = request.form.get('regimen_salud')
            ficha.eps = request.form.get('eps')
            ficha.eps_otro = request.form.get('eps_otro')
            
            # SISBEN
            ficha.registrado_sisben = request.form.get('registrado_sisben')
            ficha.grupo_sisben = request.form.get('grupo_sisben')
            ficha.pertenece_cabildo = request.form.get('pertenece_cabildo')
            ficha.nombre_cabildo = request.form.get('nombre_cabildo')
            
            # Económico
            ficha.proveedor_economico = request.form.get('proveedor_economico')
            ficha.pension = request.form.get('pension')
            ficha.pension_otro = request.form.get('pension_otro')
            ficha.subsidio = request.form.get('subsidio')
            ficha.subsidio_otro = request.form.get('subsidio_otro')
            ficha.otro_ingreso = request.form.get('otro_ingreso')
            ficha.otro_ingreso_otro = request.form.get('otro_ingreso_otro')
            ficha.administra_ingresos = request.form.get('administra_ingresos')
            ficha.destino_ingresos = request.form.get('destino_ingresos')
            
            # Vivienda
            ficha.tipo_vivienda = request.form.get('tipo_vivienda')
            ficha.estado_vivienda = request.form.get('estado_vivienda')
            ficha.hacinamiento = get_boolean('hacinamiento')
            ficha.numero_banos = get_int('numero_banos', 0)
            ficha.servicios = request.form.get('servicios')
            
            # Actividades
            ficha.participa_actividades = get_boolean('participa_actividades')
            ficha.actividades_cuales = request.form.get('actividades_cuales')
            ficha.uso_tiempo_libre = request.form.get('uso_tiempo_libre')
            ficha.centro_vida = get_boolean('centro_vida')
            ficha.centro_vida_cual = request.form.get('centro_vida_cual')
            
            # Víctimas
            ficha.victima_conflicto = get_boolean('victima_conflicto')
            ficha.certificado_victima = get_boolean('certificado_victima')
            
            # Observaciones
            ficha.observaciones = request.form.get('observaciones')
            ficha.familiar_usuario = request.form.get('familiar_usuario')
            ficha.responsable_funcionario = request.form.get('responsable_funcionario')

            db.session.commit()
            logger.info(f'Adulto mayor {id} actualizado exitosamente')
            flash('Registro actualizado exitosamente!', 'success')
            return redirect(url_for('ver_adulto_mayor', id=id))

        except Exception as e:
            db.session.rollback()
            logger.error(f'Error al actualizar adulto mayor {id}: {str(e)}', exc_info=True)
            flash(f'Error al actualizar el registro: {str(e)}', 'danger')

    return render_template('adulto_mayor/editar.html', ficha=ficha)

@app.route('/adulto-mayor/<int:id>')
def ver_adulto_mayor(id):
    ficha = FichaAdultoMayor.query.get_or_404(id)
    return render_template('adulto_mayor/ver.html', ficha=ficha)

@app.route('/adulto-mayor/lista')
def lista_adultos_mayores():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', '')

    query = FichaAdultoMayor.query
    if busqueda:
        query = query.filter(
            FichaAdultoMayor.nombres_apellidos.ilike(f'%{busqueda}%') |
            FichaAdultoMayor.numero_identificacion.ilike(f'%{busqueda}%')
        )

    adultos = query.order_by(FichaAdultoMayor.nombres_apellidos.asc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('adulto_mayor/lista.html', adultos=adultos, busqueda=busqueda)

@app.route('/adulto-mayor/eliminar/<int:id>', methods=['POST'])
def eliminar_adulto_mayor(id):
    try:
        ficha = FichaAdultoMayor.query.get_or_404(id)
        db.session.delete(ficha)
        db.session.commit()
        logger.info(f'Adulto mayor {id} eliminado exitosamente')
        flash('Registro eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error al eliminar adulto mayor {id}: {str(e)}')
        flash('Error al eliminar el registro', 'danger')
    
    return redirect(url_for('lista_adultos_mayores'))

# Ruta de debugging para verificar la base de datos
@app.route('/debug/test-db')
def test_db():
    try:
        # Intentar una consulta simple
        count = FichaAdultoMayor.query.count()
        return jsonify({
            "success": True, 
            "message": f"Base de datos conectada. Total de registros: {count}",
            "campos_modelo": [column.name for column in FichaAdultoMayor.__table__.columns]
        })
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e)
        })

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            logger.info("Tablas creadas correctamente.")
        except Exception as e:
            logger.error(f"Error al crear tablas: {str(e)}")
    
    app.run(debug=True)