# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/formularios_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123'
