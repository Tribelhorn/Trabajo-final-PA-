from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from modules.db import db
#from models.usuario import Usuario
import bcrypt 

"""
app = Flask(__name__)

#indica la ruta donde se crea la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)
"""

class Departamento(db.Model):
    n_dpto=db.Column(db.Integer(), primary_key=True)
    nombre_dpto=db.Column(db.String(66), unique=True, nullable=False)
    n_usuario = db.Column(db.Integer(), db.ForeignKey("jefes.n_usuario", deferrable=True, initially='deferred'))
    #jefe_dpto = db.relationship("Jefe", back_populates="departamento", lazy='dynamic', uselist=False)
    reclamos_dpto=db.relationship("Reclamo", back_populates="departamento", lazy='dynamic')
    keywords = db.Column(db.String(666))
    def __init__(self, nombre):
        self.nombre_dpto = nombre
        self.keywords = ""
    def asignar_jefe(self, jefe):
        self.jefe_dpto = jefe.n_usuario
    def asignar_reclamo(self, Reclamo):
        if Reclamo not in self.reclamos_dpto:
            self.reclamos_dpto.append(Reclamo)
        else:
            pass
    def cargar_keywords(self, texto):
        self.keywords = texto



class Usuario(db.Model):
    n_usuario = db.Column(db.Integer(), primary_key=True)
    nombre_usuario = db.Column(db.String(66), unique=True, nullable=False)
    correo = db.Column(db.String(66), unique=True, nullable=False)
    contraseña = db.Column(db.String(66), nullable=False)
    nombre_de_pila = db.Column(db.String(66))
    #dni = db.Column(db.Integer())
    edad = db.Column(db.Integer())
    tipo_usuario = db.Column(db.String(66))
    """usuario_final=db.relationship("Usuario_Final", uselist=False,
        back_populates="usuario",cascade="all, delete-orphan", lazy='dynamic')
    jefe=db.relationship("Jefe", uselist=False,
        back_populates="jefe",cascade="all, delete-orphan", lazy='dynamic')
    secretario=db.relationship("Secretario", uselist=False,
        back_populates="secretario",cascade="all, delete-orphan", lazy='dynamic')"""
    
    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'with_polymorphic': '*',
        "polymorphic_on": tipo_usuario}
    


    #claustro = db.Column(db.String(66))
    #reclamos_creados = db.relationship('Reclamo', back_populates='creador')#, lazy='dynamic')
    #adhesiones = db.relationship('Reclamo', back_populates='usuarios_adheridos')#, lazy='dynamic')
    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, edad):
        self.nombre_usuario = nombre_usuario 
        self.correo = correo
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Encripta la contraseña antes de ser guardada en la base de datos
        self.nombre_de_pila = nombre_de_pila
        #self.dni = dni
        self.edad = edad
        #self.claustro = claustro
        #self.reclamos_creados = []

    def check_password(self, contraseña):
        return bcrypt.checkpw(contraseña.encode('utf-8'), self.contraseña.encode('utf-8'))

class Usuario_Final(Usuario):
    n_usuario= db.mapped_column(db.Integer(), db.ForeignKey(Usuario.n_usuario), primary_key=True, use_existing_column=True)

    claustro = db.Column(db.String(66))
    reclamos_creados = db.relationship('Reclamo', back_populates='creador', lazy='dynamic')
    adhesiones = db.relationship('Reclamo', back_populates='usuarios_adheridos', secondary='adhesiones', lazy='dynamic')
    #usuario=db.relationship("Usuario", uselist=False, back_populates="usuario_final",cascade="all, delete-orphan", lazy='dynamic')

    #Ésta configuracion permite que al intanciar una clase hija se almacene en la tabla de usuario 
    __mapper_args__ = {
        'polymorphic_identity': 'final',
        'with_polymorphic': '*'}
        #'inherit_condition': (n_usuario == Usuario.n_usuario)}

    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, edad, claustro):
        super().__init__ (nombre_usuario, correo, contraseña, nombre_de_pila, edad)
        self.claustro = claustro
        self.tipo_usuario = "final"


class Jefe(Usuario):
    __tablename__ = "jefes"
    n_usuario= db.mapped_column(db.Integer(), db.ForeignKey(Usuario.n_usuario), primary_key=True,  use_existing_column=True)
    #jefe_id = db.Column(db.Integer(), primary_key=True)
    n_dpto=db.Column(db.Integer(), db.ForeignKey(Departamento.n_dpto, deferrable=True, initially='deferred'))
    #departamento = db.relationship(Departamento, back_populates="jefe_dpto", lazy='dynamic', uselist=False)#, uselist=False)
    #__mapper_args__ = {'inherit_condition': (jefe_id == Usuario.n_usuario)}
    #usuario=db.relationship("Usuario", uselist=False, back_populates="jefe", lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'jefe',
        'with_polymorphic': '*'}
        #'inherit_condition': (n_usuario == Usuario.n_usuario)}

    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, edad, departamento):
        super().__init__(nombre_usuario, correo, contraseña, nombre_de_pila, edad)
        departamento.asignar_jefe(self)
        self.departamento = departamento.n_dpto
        self.tipo_usuario = "jefe"

class Secretario(Usuario):
    n_usuario= db.mapped_column(db.Integer(), db.ForeignKey(Usuario.n_usuario), primary_key=True,  use_existing_column=True)

    __mapper_args__ = {
        'polymorphic_identity': 'secretario',
        'with_polymorphic': '*'}
        #'inherit_condition': (n_usuario == Usuario.n_usuario)}

    def __init__(self, nombre_usuario, correo, contraseña, nombre_de_pila, edad):
        super().__init__ (nombre_usuario, correo, contraseña, nombre_de_pila, edad)
        self.tipo_usuario = "secretario"
    





class Reclamo(db.Model):
    codigo = db.Column(db.Integer(), primary_key=True)
    asunto = db.Column(db.String(66), nullable=False)
    texto = db.Column(db.String(666), nullable=False)
    estado = db.Column(db.String(66), nullable=False)
    fecha = db.Column(db.String(66))
    imagen= db.Column(db.LargeBinary)
    n_dpto= db.Column(db.Integer, db.ForeignKey(Departamento.n_dpto, deferrable=True, initially='deferred'))
    departamento = db.relationship("Departamento", back_populates="reclamos_dpto")
    creador_id = db.Column(db.Integer, db.ForeignKey(Usuario_Final.n_usuario, deferrable=True, initially='deferred'))
    creador = db.relationship('Usuario_Final', back_populates='reclamos_creados')
    usuarios_adheridos = db.relationship('Usuario_Final', secondary='adhesiones', back_populates='adhesiones', lazy='dynamic')

    def __init__(self, asunto, texto,  creador_id):
        self.texto = texto
        self.asunto = asunto
        self.creador_id = creador_id
        self.creador = Usuario.query.filter_by(n_usuario=creador_id).first()
        self.estado = "Pendiente"
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.usuarios_adheridos = []

    def añadir_imagen(self, imagen):
        self.imagen = imagen

    def adherir(self, usuario_id):
        #try:
            usuario = Usuario.query.filter_by(n_usuario=usuario_id).first()
            if usuario in self.usuarios_adheridos:
                pass
            elif self.creador_id != usuario_id:
                self.usuarios_adheridos.append(usuario)
                db.session.commit()
        #except:
        #    raise InterruptedError



adhesiones = db.Table('adhesiones',
    db.Column('usuario_id', db.Integer, db.ForeignKey(Usuario_Final.n_usuario, deferrable=True, initially='deferred')),
    db.Column('reclamo_codigo', db.Integer, db.ForeignKey(Reclamo.codigo, deferrable=True, initially='deferred')))