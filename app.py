from flask import Flask, render_template, request, redirect, url_for, flash
from models import db
from config import Config
from models import Inclusion
from flask_migrate import Migrate

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
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        email = request.form['email']
        tiene_discapacidad = request.form['tiene_discapacidad']
        incapacidad = request.form['incapacidad']

        nueva = Inclusion(
            nombre=nombre,
            cedula=cedula,
            email=email,
            tiene_discapacidad=tiene_discapacidad,
            incapacidad=incapacidad
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Inclusión registrada con éxito', 'success')
        return redirect(url_for('lista_inclusiones'))

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tablas creadas correctamente.")
    app.run(debug=True)
