from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.db import db
#from models.usuario import Usuario
import bcrypt 

"""
app = Flask(__name__)

#indica la ruta donde se crea la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)
"""
class Departamento(db.Model):
    n_dpto=db.Column(db.Integer, primary_key=True)
    nombre_dpto=db.Column(db.String(66), unique=True, nullable=False)
    jefe_dpto=db.Column(db.Integer, db.ForeignKey("Jefe.n_usuario"), uselist=False)
    def __init__(self, nombre):
        self.nombre_dpto = nombre
    def asignar_jefe(self, jefe):
        self.jefe_dpto = jefe.n_usuario

class Usuario(db.Model):
    n_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(66), unique=True, nullable=False)
    correo = db.Column(db.String(66), unique=True, nullable=False)
    contraseña = db.Column(db.String(66), nullable=False)
    nombre_de_pila = db.Column(db.String(66))
    dni = db.Column(db.Integer())
    edad = db.Column(db.Integer())
    #claustro = db.Column(db.String(66))
    #reclamos_creados = db.relationship('Reclamo', back_populates='creador')#, lazy='dynamic')
    #adhesiones = db.relationship('Reclamo', back_populates='usuarios_adheridos')#, lazy='dynamic')
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad
        #self.claustro = claustro
       # self.reclamos_creados = []

    def check_password(self, contraseña):
        return bcrypt.checkpw(contraseña.encode('utf-8'), self.contraseña.encode('utf-8'))

class Usuario_Final(Usuario):
    claustro = db.Column(db.String(66))
    reclamos_creados = db.relationship('Reclamo', back_populates='creador')#, lazy='dynamic')
    adhesiones = db.relationship('Reclamo', back_populates='usuarios_adheridos')#, lazy='dynamic')
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad, claustro):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad
        self.claustro = claustro
        self.reclamos_creados = []
        self.adhesiones = []

class Jefe(Usuario):
    departamento=  db.Column(db.Integer, db.ForeignKey("Departamento.n_departamento"), uselist=False)
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad, departamento):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad
        departamento.asignar_jefe(self)
        departamento = departamento.n_dpto

class Secretario(Usuario):
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        self.dni = dni
        self.edad = edad

class Reclamo(db.Model):
    codigo = db.Column(db.Integer(), primary_key=True)
    texto = db.Column(db.String(666), nullable=False)
    estado = db.Column(db.String(66), nullable=False)
    fecha = db.Column(db.DateTime())
    departamento = db.relationship('Departamento', back_populates='reclamos_dpto')
    creador_id = db.Column(db.Integer, db.ForeignKey(Usuario.n_usuario))
    creador = db.relationship('Usuario_Final', back_populates='reclamos_creados')
    usuarios_adheridos = db.relationship('Usuario_Final', secondary='adhesiones', back_populates='adhesiones')

    def __init__(self, texto, creador):
        self.texto = texto
        self.creador = creador
        self.estado = "Pendiente"
        self.fecha = datetime.now()
        self.usuarios_adheridos = []

adhesiones = db.Table('adhesiones',
    db.Column('usuario_id', db.Integer, db.ForeignKey(Usuario_Final.n_usuario)),
    db.Column('reclamo_codigo', db.Integer, db.ForeignKey(Reclamo.codigo)))