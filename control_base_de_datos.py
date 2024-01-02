import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)

usuario_reclamo = db.Table("usuario_reclamo", db.Column('n_usuario', db.Integer, db.ForeignKey('usuario.n_usuario'), primary_key=True), db.Column('codigo_reclamo', db.Integer, db.ForeignKey('reclamo.codigo'), primary_key=True) )

class Usuario(db.Model):
    n_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String())
    reclamos = db.relationship('Reclamo', secondary=usuario_reclamo, backref = db.backref('usuarios adheridos'))

class Reclamo(db.Model):
    codigo = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String, primary_key=True)
    creador = db.relationship('Usuario', backref=db.backref('mis_reclamos', lazy=True))


"""

# Conectar a la base de datos (creará el archivo si no existe)
conn = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Ejemplo: Crear una tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        email TEXT
    )
''')

# Guardar los cambios
conn.commit()

cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", ('Juan Pérez', 'juan@email.com'))
conn.commit()

# Leer todos los usuarios
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()
print(usuarios)

# Actualizar un usuario
cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", ('Juan González', 1))
conn.commit()

# Eliminar un usuario
#cursor.execute("DELETE FROM usuarios WHERE id = ?", (1,))
#conn.commit()

"""