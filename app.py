#Importamos la clase Flask, url_for sirve para redireccionar 
from flask import Flask, render_template, request, redirect, url_for, session
#from models.usuario_reclamo import *
from models.reclamo import *
from models.usuario import *
from flask_sqlalchemy import SQLAlchemy
#Instanciamos un objeto app de la calse Flask con el argumento __name__ que indica la ubicación del archivo 
app = Flask(__name__)

app.secret_key="cvbnmrtyuiop"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)

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
                nombre_usuario = request.form['nombre_usuario']
                contraseña = request.form['contraseña']
                correo= request.form['correo']
                nombre_de_pila = request.form['n_y_a']
                dni = int(request.form['dni'])
                edad = int(request.form['edad'])
                claustro = request.form['claustro']
                new_user = Usuario(nombre_usuario, correo, contraseña, nombre_de_pila, dni, edad, claustro)
                db.session.add(new_user)
                db.session.commit()
                print("HOLA PUTOS")
                return redirect("login.html") #registro exitoso
            except Exception:       
                render_template("registro.html") #ingrese datos válidos
        else:
            return render_template("registro.html")  #no coinciden las contraseñas
    return render_template("registro.html") 

#render_template renderiza una plantilla html
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
    
        usuario = Usuario.query.filter_by(nombre_usuario).first()

        if usuario and nombre_usuario.check_password(contraseña):
            session['nombre_usuario']=usuario.nombre_usuario
            session['contraseña']=usuario.contraseña
            session['nombre_de_pila']=usuario.nombre_de_pila
            session['edad']=usuario.edad
            session['claustro']=usuario.claustro
            session['correo']=usuario.correo
            return render_template("inicio.html")
        else:
            return render_template("login.html") #usuario no válido o contraseña incorrecta
    
    return render_template("login.html")        


@app.route("/inicio", methods=["GET","POST"])   
def inicio():
    if session["claustro"] == "alumno" or "profe" or "pays":
        return render_template("inicio.html", session["nombre_usuario"], session["nombre_de_pila"], session["edad"])
    elif session["claustro"] == "jefe":
        return render_template("inicio_2.html")
    elif session["claustro"] == "secretario":
        return render_template("inicio_2.html")
    else:
        return render_template("login.html")


#Éstas líneas corren el programa de manera "continua"
if __name__ == "__main__":
    app.run(debug=True)
