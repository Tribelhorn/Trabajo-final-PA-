#Importamos la clase Flask, url_for sirve para redireccionar 
from flask import Flask, render_template, request, redirect, url_for, session
#from models.usuario_reclamo import *
from models.clases import Usuario, Reclamo, adhesiones
#from models.usuario import *
from flask_sqlalchemy import SQLAlchemy
from models.db import db, app

#Instanciamos un objeto app de la calse Flask con el argumento __name__ que indica la ubicación del archivo 
#app = Flask(__name__)

app.secret_key="cvbnmrtyuiop"

"""app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)
"""
#Crea laa base de datos 
with app.app_context():
    db.create_all()


##Definimos la función hola() con el decorador app.route que indica en la ruta "/"
#@app.route("/")
#def hola():
#    return "Hola mundo"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        
        if request.form['contraseña'] == request.form['r_contraseña']:

            try:
                nombre_usuario = request.form.get('nombre_usuario')
                contraseña = request.form.get('contraseña')
                correo= request.form.get('correo')
                nombre_de_pila = request.form.get('n_y_a')
                dni = int(request.form.get('dni'))
                edad = int(request.form.get('edad'))
                claustro = request.form.get('claustro')
                new_user = Usuario(nombre_usuario=nombre_usuario, correo=correo, contraseña=contraseña, nombre_de_pila=nombre_de_pila, dni=dni, edad=edad, claustro=claustro)
                db.session.add(new_user)
                db.session.commit()

                return render_template("login.html") #registro exitoso
            except Exception:       
              return render_template("registro.html")#, Mensaje #ingrese datos válidos
        else:
            return render_template("registro.html")  #no coinciden las contraseñas
    return render_template("registro.html") 

#render_template renderiza una plantilla html
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

        if usuario and usuario.check_password(contraseña):
            session['nombre_usuario']=usuario.nombre_usuario
            session['contraseña']=usuario.contraseña
            session['nombre_de_pila']=usuario.nombre_de_pila
            session['edad']=usuario.edad
            session['claustro']=usuario.claustro
            session['correo']=usuario.correo

            return redirect("/inicio")
        else:
            return render_template("login.html") #usuario no válido o contraseña incorrecta
    
    return render_template("login.html")        


@app.route("/inicio", methods=["GET","POST"])   
def inicio():
    print (session['claustro'])
    if session["claustro"] == "alumno" or session["claustro"] == "profe" or session["claustro"] == "pays":
        print("Alooooooo")
        return render_template("inicio.html") #session["nombre_usuario"], session["nombre_de_pila"], session["edad"])
    elif session["claustro"] == "jefe":
        return render_template("inicio_2.html")
    elif session["claustro"] == "secretario":
        return render_template("inicio_2.html")
    else:
        return render_template("login.html")


#Éstas líneas corren el programa de manera "continua"
if __name__ == "__main__":
    app.run(debug=True)
