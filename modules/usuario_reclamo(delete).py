from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#indica la ruta donde se crea la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)

#Tabla relacional entre usuario y reclamo 
usuario_reclamo = db.Table("usuario_reclamo", db.Column('n_usuario', db.Integer, db.ForeignKey('usuario.n_usuario'), primary_key=True), db.Column('codigo_reclamo', db.Integer, db.ForeignKey('reclamo.codigo'), primary_key=True) )
