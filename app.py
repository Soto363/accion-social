from sqlalchemy.exc import IntegrityError 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Inclusion, InformacionGeneral, Contacto, FamiliaRedApoyo, EducacionOcupacion, Salud, SeguridadSocial, DatosSocioeconomicos, Vivienda, Actividades, UnidadVictimas, Observaciones
from config import Config
from flask_migrate import Migrate
from datetime import datetime
import re

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return redirect(url_for('lista_inclusiones'))

@app.route('/inclusion', methods=['GET', 'POST'])
def crear_inclusion():
    if request.method == 'POST':
        try:
            # Determinar si es JSON o form-data
            is_json = request.is_json
            data = request.get_json() if is_json else request.form
            
            # Obtener datos
            nombre = data.get('nombre', '').strip()
            cedula = data.get('cedula', '').strip()
            email = data.get('email', '').strip()
            tiene_discapacidad = data.get('tiene_discapacidad', '')
            incapacidad = data.get('incapacidad', '')

            # Validaciones
            errores = {}
            
            if not nombre or len(nombre) < 3:
                errores['nombre'] = 'El nombre debe tener al menos 3 caracteres'
            
            if not cedula or not cedula.isdigit() or len(cedula) < 6:
                errores['cedula'] = 'La cédula debe tener al menos 6 dígitos numéricos'
                
            if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                errores['email'] = 'Formato de email inválido'
                
            if not tiene_discapacidad:
                errores['tiene_discapacidad'] = 'Seleccione una opción'
                
            if tiene_discapacidad == 'Si' and not incapacidad:
                errores['incapacidad'] = 'Seleccione un tipo de discapacidad'

            if errores:
                app.logger.debug(f'Errores de validación: {errores}')
                return jsonify({
                    'success': False,
                    'errors': errores
                }), 400

            # Crear nuevo registro
            nueva_inclusion = Inclusion(
                nombre=nombre,
                cedula=cedula,
                email=email if email else None,
                tiene_discapacidad=tiene_discapacidad,
                incapacidad=incapacidad if tiene_discapacidad == 'Si' else None
            )
            
            db.session.add(nueva_inclusion)
            db.session.commit()

            app.logger.debug('Registro creado exitosamente')
            return jsonify({
                'success': True,
                'message': 'Registro guardado exitosamente!',
                'redirect': url_for('lista_inclusiones')
            })

        except IntegrityError as e:
            db.session.rollback()
            app.logger.error(f'Error de integridad: {str(e)}')
            return jsonify({
                'success': False,
                'errors': {'cedula': 'Esta cédula ya está registrada'}
            }), 400

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error inesperado: {str(e)}')
            return jsonify({
                'success': False,
                'error': 'Error interno del servidor. Por favor intente nuevamente.'
            }), 500

    return render_template('inclusion/create.html')

@app.route('/inclusiones')
def lista_inclusiones():
    pagina = request.args.get('pagina', 1, type=int)
    busqueda = request.args.get('busqueda', '', type=str)

    query = Inclusion.query

    if busqueda:
        query = query.filter(
            Inclusion.nombre.ilike(f'%{busqueda}%') |
            Inclusion.cedula.ilike(f'%{busqueda}%')
        )

    inclusiones = query.order_by(Inclusion.nombre.asc()).paginate(page=pagina, per_page=5)

    return render_template('inclusion/index_inclusion.html', inclusiones=inclusiones, busqueda=busqueda)


@app.route('/inclusion/editar/<int:id>', methods=['GET', 'POST'])
def editar_inclusion(id):
    inclusion = Inclusion.query.get_or_404(id)

    if request.method == 'POST':
        inclusion.nombre = request.form['nombre']
        inclusion.cedula = request.form['cedula']
        inclusion.email = request.form['email']
        inclusion.tiene_discapacidad = request.form['tiene_discapacidad']
        inclusion.incapacidad = request.form['incapacidad']

        db.session.commit()
        flash('Inclusión actualizada correctamente.', 'success')
        return redirect(url_for('lista_inclusiones'))

    return render_template('inclusion/edit.html', inclusion=inclusion)

@app.route('/inclusion/eliminar/<int:id>', methods=['POST'])
def eliminar_inclusion(id):
    inclusion = Inclusion.query.get_or_404(id)
    db.session.delete(inclusion)
    db.session.commit()
    flash('Inclusión eliminada con éxito.', 'success')
    return redirect(url_for('lista_inclusiones'))

#rutas adulto mayor
@app.route('/adulto-mayor/nuevo', methods=['GET', 'POST'])
def nuevo_adulto_mayor():
    if request.method == 'POST':
        try:
            # Crear registro principal
            nueva_inclusion = Inclusion(
                nombre=request.form.get('nombre'),
                cedula=request.form.get('cedula'),
                email=request.form.get('email'),
                tiene_discapacidad=request.form.get('tiene_discapacidad', 'No'),
                incapacidad=request.form.get('incapacidad')
            )
            db.session.add(nueva_inclusion)
            db.session.flush()  # Para obtener el ID
            
            # Información General
            fecha_nac = datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None
            info_general = InformacionGeneral(
                inclusion_id=nueva_inclusion.id,
                fecha_aplicacion=datetime.now().date(),
                tipo_identificacion=request.form.get('tipo_identificacion'),
                sexo=request.form.get('sexo'),
                fecha_nacimiento=fecha_nac,
                zona_residencia=request.form.get('zona_residencia'),
                barrio_vereda=request.form.get('barrio_vereda'),
                direccion_residencia=request.form.get('direccion_residencia')
            )
            db.session.add(info_general)
            
            # Contacto
            contacto = Contacto(
                inclusion_id=nueva_inclusion.id,
                numero_contacto=request.form.get('numero_contacto'),
                estado_civil=request.form.get('estado_civil')
            )
            db.session.add(contacto)
            
            # Familia y Red de Apoyo
            familia = FamiliaRedApoyo(
                inclusion_id=nueva_inclusion.id,
                vive_con=request.form.get('vive_con')
            )
            db.session.add(familia)
            
            # Educación y Ocupación
            educacion = EducacionOcupacion(
                inclusion_id=nueva_inclusion.id,
                ocupacion_actual=request.form.get('ocupacion_actual'),
                nivel_escolaridad=request.form.get('nivel_escolaridad'),
                sabe_leer_escribir=request.form.get('sabe_leer_escribir') == 'true',
                educacion_informal=request.form.get('educacion_informal') == 'true',
                tipo_educacion_informal=request.form.get('tipo_educacion_informal')
            )
            db.session.add(educacion)
            
            # Salud
            salud = Salud(
                inclusion_id=nueva_inclusion.id,
                enfermedad_fisica_mental=request.form.get('enfermedad_fisica_mental') == 'true',
                descripcion_enfermedad=request.form.get('descripcion_enfermedad'),
                tiempo_con_enfermedad=request.form.get('tiempo_con_enfermedad'),
                recibe_tratamiento=request.form.get('recibe_tratamiento') == 'true',
                tratamiento=request.form.get('tratamiento'),
                frecuencia_medico=request.form.get('frecuencia_medico'),
                tipo_discapacidad=request.form.get('tipo_discapacidad'),
                certificado_discapacidad=request.form.get('certificado_discapacidad') == 'true',
                controles_periodicos=request.form.get('controles_periodicos') == 'true'
            )
            db.session.add(salud)
            
            # Seguridad Social
            seguridad = SeguridadSocial(
                inclusion_id=nueva_inclusion.id,
                afiliado_salud=request.form.get('afiliado_salud') == 'true',
                regimen_salud=request.form.get('regimen_salud'),
                eps=request.form.get('eps')
            )
            db.session.add(seguridad)
            
            # Datos Socioeconómicos
            socioeconomicos = DatosSocioeconomicos(
                inclusion_id=nueva_inclusion.id,
                registrado_sisben=request.form.get('registrado_sisben') == 'true',
                grupo_sisben=request.form.get('grupo_sisben'),
                pertenece_cabildo=request.form.get('pertenece_cabildo') == 'true',
                nombre_cabildo=request.form.get('nombre_cabildo'),
                proveedor_economico=request.form.get('proveedor_economico'),
                tipo_pension=request.form.get('tipo_pension'),
                tipo_subsidio=request.form.get('tipo_subsidio'),
                otros_ingresos=request.form.get('otros_ingresos'),
                quien_administra_ingresos=request.form.get('quien_administra_ingresos'),
                prioridades_ingresos=request.form.get('prioridades_ingresos')
            )
            db.session.add(socioeconomicos)
            
            # Vivienda
            vivienda = Vivienda(
                inclusion_id=nueva_inclusion.id,
                tipo_vivienda=request.form.get('tipo_vivienda'),
                estado_vivienda=request.form.get('estado_vivienda'),
                vive_hacinamiento=request.form.get('vive_hacinamiento') == 'true',
                numero_banos=int(request.form.get('numero_banos', 0)),
                servicios=request.form.get('servicios')
            )
            db.session.add(vivienda)
            
            # Actividades
            actividades = Actividades(
                inclusion_id=nueva_inclusion.id,
                participa_actividades=request.form.get('participa_actividades') == 'true',
                tipo_actividades=request.form.get('tipo_actividades'),
                tiempo_libre=request.form.get('tiempo_libre'),
                participa_centro_vida=request.form.get('participa_centro_vida') == 'true',
                cual_centro=request.form.get('cual_centro')
            )
            db.session.add(actividades)
            
            # Unidad de Víctimas
            victimas = UnidadVictimas(
                inclusion_id=nueva_inclusion.id,
                es_victima=request.form.get('es_victima') == 'true',
                tiene_certificado=request.form.get('tiene_certificado') == 'true'
            )
            db.session.add(victimas)
            
            # Observaciones
            obs = Observaciones(
                inclusion_id=nueva_inclusion.id,
                observaciones=request.form.get('observaciones'),
                usuario=request.form.get('usuario'),
                familiar_usuario=request.form.get('familiar_usuario'),
                responsable_ficha=request.form.get('responsable_ficha')
            )
            db.session.add(obs)
            
            db.session.commit()
            flash('Registro de adulto mayor creado exitosamente!', 'success')
            return redirect(url_for('lista_adultos_mayores'))
            
        except IntegrityError:
            db.session.rollback()
            flash('Error: La cédula ya está registrada', 'danger')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error al crear adulto mayor: {str(e)}')
            flash('Error al guardar el registro', 'danger')
    
    return render_template('adulto_mayor/nuevo.html')

@app.route('/adulto-mayor/editar/<int:id>', methods=['GET', 'POST'])
def editar_adulto_mayor(id):
    inclusion = Inclusion.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar registro principal
            inclusion.nombre = request.form.get('nombre')
            inclusion.email = request.form.get('email')
            inclusion.tiene_discapacidad = request.form.get('tiene_discapacidad', 'No')
            inclusion.incapacidad = request.form.get('incapacidad')
            
            # Actualizar todas las tablas relacionadas...
            # (Similar al código de creación pero con updates)
            
            db.session.commit()
            flash('Registro actualizado exitosamente!', 'success')
            return redirect(url_for('ver_adulto_mayor', id=id))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error al actualizar adulto mayor: {str(e)}')
            flash('Error al actualizar el registro', 'danger')
    
    return render_template('adulto_mayor/editar.html', inclusion=inclusion)

@app.route('/adulto-mayor/<int:id>')
def ver_adulto_mayor(id):
    inclusion = Inclusion.query.get_or_404(id)
    return render_template('adulto_mayor/ver.html', inclusion=inclusion)

@app.route('/adulto-mayor/lista')
def lista_adultos_mayores():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', '')
    
    query = Inclusion.query
    
    if busqueda:
        query = query.filter(
            Inclusion.nombre.ilike(f'%{busqueda}%') |
            Inclusion.cedula.ilike(f'%{busqueda}%')
        )
    
    adultos = query.order_by(Inclusion.nombre).paginate(page=page, per_page=10)
    return render_template('adulto_mayor/lista.html', adultos=adultos, busqueda=busqueda)

@app.route('/adulto-mayor/eliminar/<int:id>', methods=['POST'])
def eliminar_adulto_mayor(id):
    inclusion = Inclusion.query.get_or_404(id)
    db.session.delete(inclusion)
    db.session.commit()
    flash('Registro eliminado exitosamente', 'success')
    return redirect(url_for('lista_adultos_mayores'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tablas creadas correctamente.")
    app.run(debug=True)
