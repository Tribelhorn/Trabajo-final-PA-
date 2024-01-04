from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from usuario_reclamo import usuario_reclamo
import bcrypt 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)

usuario_reclamo = db.Table("usuario_reclamo", db.Column('n_usuario', db.Integer, db.ForeignKey('usuario.n_usuario'), primary_key=True), db.Column('codigo_reclamo', db.Integer, db.ForeignKey('reclamo.codigo'), primary_key=True) )

class Usuario(db.Model):
    n_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(), unique=True, nullable=False)
    correo = db.Column(db.String(), unique=True, nullable=False)
    contraseña = db.Column(db.String(), nullable=False)
    nombre_de_pila = db.Column(db.String())
    dni = db.Column(db.Integer())
    edad = db.Column(db.Integer())
    claustro = db.Column(db.String())
    reclamos = db.relationship('Reclamo', secondary=usuario_reclamo, backref = db.backref('usuarios adheridos'))
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad, claustro):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad
        self.claustro = claustro

    def check_password(self, contraseña):
        return bcrypt.checkpw(contraseña.encode('utf-8'), self.contraseña.encode('utf-8'))
    
#class Usuario_Final(Usuario):
#    reclamos = db.relationship('Reclamo', secondary=usuario_reclamo, backref = db.backref('usuarios adheridos'))

"""
class Jefe(Usuario):
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad
        self.claustro = "jefe"

class Secretario(Usuario):
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad
        self.claustro = "secretario"
"""

