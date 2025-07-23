# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/forms_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12345'
