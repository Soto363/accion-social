from app import app, db
from models import Administrador
from werkzeug.security import generate_password_hash

def reset_database():
    with app.app_context():
        # Elimina y recrea todas las tablas
        db.drop_all()
        db.create_all()
        
        # Crea un administrador de prueba
        admin = Administrador(
            nombre='Admin Reseteado',
            email='admin@reseteado.com',
            usuario='admin',
            contrasena=generate_password_hash('NuevaContraseña123!')
        )
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Base de datos reseteada")
        print("Usuario: admin")
        print("Contraseña: NuevaContraseña123!")

if __name__ == '__main__':
    reset_database()