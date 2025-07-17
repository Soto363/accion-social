from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config  

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ✅ Aquí defines el modelo
class Inclusion(db.Model):
    __tablename__ = 'inclusiones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    tiene_discapacidad = db.Column(db.String(5), nullable=False)
    incapacidad = db.Column(db.String(100), nullable=True)

# ✅ Luego creas las tablas
with app.app_context():
    db.create_all()
