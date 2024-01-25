#Importamos la clase Flask, url_for sirve para redireccionar 
from flask import Flask, render_template, request, redirect, url_for, session
#from models.usuario_reclamo import *
from modules.clases import Usuario, Usuario_Final, Jefe, Secretario, Reclamo, adhesiones, Departamento 
#from models.usuario import *
from flask_sqlalchemy import SQLAlchemy
from modules.db import db, app

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
                new_user = Usuario_Final(nombre_usuario=nombre_usuario, correo=correo, contraseña=contraseña, nombre_de_pila=nombre_de_pila, dni=dni, edad=edad, claustro=claustro)
            
                with app.app_context():
                    db.session.add(new_user)
                    db.session.commit()
                return redirect("/") #registro exitoso
            except Exception:       
                return render_template("registro.html") #, Mensaje #ingrese datos válidos
        else:
            return render_template("registro.html") #no coinciden las contraseñas
    return render_template("registro.html") 

#render_template renderiza una plantilla html
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

        if usuario.tipo_usuario == "final" and usuario.check_password(contraseña):
            print("FINAL")  
            n_usuario = usuario.n_usuario
            usuario_f = Usuario_Final.query.filter_by(n_usuario=n_usuario).first()
            print (usuario_f.nombre_de_pila)
            session['nombre_usuario']=usuario_f.nombre_usuario
            session['contraseña']=usuario_f.contraseña
            session['nombre_de_pila']=usuario_f.nombre_de_pila
            session['edad']=usuario_f.edad
            session['claustro']=usuario_f.claustro
            session['correo']=usuario_f.correo
            session['tipo_usuario'] =usuario_f.tipo_usuario
            return redirect("/inicio")
        
        elif usuario.tipo_usuario == "jefe" and usuario.check_password(contraseña):
            #print("JEFE")
            usuario = Jefe.query.filter_by(nombre_usuario=nombre_usuario).first()
            session['nombre_usuario']=usuario.nombre_usuario
            session['contraseña']=usuario.contraseña
            session['nombre_de_pila']=usuario.nombre_de_pila
            session['edad']=usuario.edad
            session['correo']=usuario.correo
            session['tipo_usuario'] =usuario.tipo_usuario
            return redirect("/inicio")
        
        elif usuario.tipo_usuario == "secretario" and usuario.check_password(contraseña):
            #print("SECRETARIO")
            usuario = Secretario.query.filter_by(nombre_usuario=nombre_usuario).first()
            session['nombre_usuario']=usuario.nombre_usuario
            session['contraseña']=usuario.contraseña
            session['nombre_de_pila']=usuario.nombre_de_pila
            session['edad']=usuario.edad
            session['correo']=usuario.correo
            session['tipo_usuario'] =usuario.tipo_usuario
            return redirect("/inicio")
        else:
            #print("No funca")
            return redirect("/") #usuario no válido o contraseña incorrecta
    
    return render_template("/login.html")        


@app.route("/inicio", methods=["GET","POST"])   
def inicio():
    if session['tipo_usuario'] == "final":
        print("Alooooooo")
        return render_template("inicio.html") #session["nombre_usuario"], session["nombre_de_pila"], session["edad"])
    elif session['tipo_usuario'] == "jefe":
        print("ola k ase")
        return render_template("inicio_2.html")
    elif session['tipo_usuario'] == "secretario":
        return render_template("inicio_2.html")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#Éstas líneas corren el programa de manera "continua"
if __name__ == "__main__":
    app.run(debug=True)
