#Importamos la clase Flask, url_for sirve para redireccionar 
from flask import Flask, render_template, url_for
from control_base_de_datos import *
from flask_sqlalchemy import SQLAlchemy
#Instanciamos un objeto app de la calse Flask con el argumento __name__ que indica la ubicación del archivo 
app = Flask(__name__)

app.secret_key="cvbnmrtyuiop"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


#Definimos la función hola() con el decorador app.route que indica en la ruta "/"
#@app.route("/")
#def hola():
#    return "Hola mundo"

#render_template renderiza una plantilla html
@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")        

#Éstas líneas corren el programa de manera "continua"
if __name__ == "__main__":
    app.run(debug=True)
