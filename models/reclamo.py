from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

#indica la ruta donde se crea la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)


class Reclamo(db.Model):
    codigo = db.Column(db.Integer(), primary_key=True)
    texto = db.Column(db.String(), primary_key=True, nullable=False)
    estado = db.Column(db.String(), nullable=False)
    fecha = db.Column(db.DateTime())
    creador = db.relationship('Usuario', backref=db.backref('mis_reclamos', lazy=True))
    def __init__(self, texto, creador):
        self.texto = texto
        self.creador = creador
        self.estado = "Pendiente"
        self.fecha = datetime.now()
