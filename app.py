from sqlalchemy.exc import IntegrityError 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, FichaAdultoMayor
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
    return redirect(url_for('lista_adultos_mayores'))

# RUTAS ADULTO MAYOR
@app.route('/adulto-mayor/nuevo', methods=['GET', 'POST'])
def nuevo_adulto_mayor():
    if request.method == 'POST':
        
        
        try:
            ficha = FichaAdultoMayor(
                fecha_aplicacion=datetime.now().date(),
                tipo_identificacion=request.form.get('tipo_identificacion'),
                otro_tipo_identificacion=request.form.get('otro_tipo_identificacion'),
                numero_identificacion=request.form.get('numero_identificacion'),
                nombres_apellidos=request.form.get('nombres_apellidos'),
                sexo=request.form.get('sexo'),
                sexo_otro=request.form.get('sexo_otro'),
                fecha_nacimiento=datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d') if request.form.get('fecha_nacimiento') else None,
                edad=request.form.get('edad'),
                zona_residencia=request.form.get('zona_residencia'),
                barrio_vereda=request.form.get('barrio_vereda'),
                direccion_residencia=request.form.get('direccion_residencia'),
                numero_contacto=request.form.get('numero_contacto'),
                estado_civil=request.form.get('estado_civil'),
                convivencia=request.form.get('convivencia'),
                convivencia_otro=request.form.get('convivencia_otro'),
                ocupacion=request.form.get('ocupacion'),
                escolaridad=request.form.get('escolaridad'),
                sabe_leer_escribir=request.form.get('sabe_leer_escribir') == 'true',
                educacion_informal=request.form.get('educacion_informal') == 'true',
                educacion_informal_cual=request.form.get('educacion_informal_cual'),
                enfermedad=request.form.get('enfermedad') == 'true',
                enfermedad_cual=request.form.get('enfermedad_cual'),
                tiempo_enfermedad=request.form.get('tiempo_enfermedad'),
                tratamiento=request.form.get('tratamiento') == 'true',
                tratamiento_cual=request.form.get('tratamiento_cual'),
                frecuencia_medico=request.form.get('frecuencia_medico'),
                discapacidad=request.form.get('discapacidad') == 'true',
                tipo_discapacidad=request.form.get('tipo_discapacidad'),
                certificado_discapacidad=request.form.get('certificado_discapacidad') == 'true',
                controles_periodicos=request.form.get('controles_periodicos') == 'true',
                afiliado_salud=request.form.get('afiliado_salud') == 'true',
                regimen_salud=request.form.get('regimen_salud'),
                eps=request.form.get('eps'),
                eps_otro=request.form.get('eps_otro'),
                registrado_sisben=request.form.get('registrado_sisben'),
                grupo_sisben=request.form.get('grupo_sisben'),
                pertenece_cabildo=request.form.get('pertenece_cabildo'),
                nombre_cabildo=request.form.get('nombre_cabildo'),
                proveedor_economico=request.form.get('proveedor_economico'),
                pension=request.form.get('pension'),
                pension_otro=request.form.get('pension_otro'),
                subsidio=request.form.get('subsidio'),
                subsidio_otro=request.form.get('subsidio_otro'),
                otro_ingreso=request.form.get('otro_ingreso'),
                otro_ingreso_otro=request.form.get('otro_ingreso_otro'),
                administra_ingresos=request.form.get('administra_ingresos'),
                destino_ingresos=request.form.get('destino_ingresos'),
                tipo_vivienda=request.form.get('tipo_vivienda'),
                estado_vivienda=request.form.get('estado_vivienda'),
                hacinamiento=request.form.get('hacinamiento') == 'true',
                numero_banos=int(request.form.get('numero_banos') or 0),
                servicios=request.form.get('servicios'),
                participa_actividades=request.form.get('participa_actividades') == 'true',
                actividades_cuales=request.form.get('actividades_cuales'),
                uso_tiempo_libre=request.form.get('uso_tiempo_libre'),
                centro_vida=request.form.get('centro_vida') == 'true',
                centro_vida_cual=request.form.get('centro_vida_cual'),
                victima_conflicto=request.form.get('victima_conflicto') == 'true',
                certificado_victima=request.form.get('certificado_victima') == 'true',
                observaciones=request.form.get('observaciones'),
                familiar_usuario=request.form.get('familiar_usuario'),
                responsable_funcionario=request.form.get('responsable_funcionario')
            )

            db.session.add(ficha)
            db.session.commit()
            flash('Ficha del adulto mayor registrada exitosamente', 'success')
            return redirect(url_for('lista_adultos_mayores'))

        except IntegrityError:
            db.session.rollback()
            flash('Error: El número de identificación ya está registrado.', 'danger')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error al guardar ficha: {str(e)}')
            flash('Error al guardar los datos.', 'danger')

    return render_template('adulto_mayor/nuevo.html')

@app.route('/adulto-mayor/editar/<int:id>', methods=['GET', 'POST'])
def editar_adulto_mayor(id):
    ficha = FichaAdultoMayor.query.get_or_404(id)

    if request.method == 'POST':
        try:
            ficha.nombres_apellidos = request.form.get('nombres_apellidos')
            ficha.numero_identificacion = request.form.get('numero_identificacion')
            ficha.discapacidad = request.form.get('discapacidad') == 'true'
            ficha.tipo_discapacidad = request.form.get('tipo_discapacidad')
            # Agrega aquí los demás campos que quieras actualizar

            db.session.commit()
            flash('Registro actualizado exitosamente!', 'success')
            return redirect(url_for('ver_adulto_mayor', id=id))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error al actualizar adulto mayor: {str(e)}')
            flash('Error al actualizar el registro', 'danger')

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

    adultos = query.order_by(FichaAdultoMayor.nombres_apellidos.asc()).paginate(page=page, per_page=10)
    return render_template('adulto_mayor/lista.html', adultos=adultos, busqueda=busqueda)

@app.route('/adulto-mayor/eliminar/<int:id>', methods=['POST'])
def eliminar_adulto_mayor(id):
    ficha = FichaAdultoMayor.query.get_or_404(id)
    db.session.delete(ficha)
    db.session.commit()
    flash('Registro eliminado correctamente', 'success')
    return redirect(url_for('lista_adultos_mayores'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tablas creadas correctamente.")
    app.run(debug=True)
