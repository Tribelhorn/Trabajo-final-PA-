#Importamos la clase Flask, url_for sirve para redireccionar 
from flask import Flask, render_template, request, redirect, url_for, session
#from models.usuario_reclamo import *
from modules.clases import Usuario, Usuario_Final, Jefe, Secretario, Reclamo, adhesiones, Departamento 
#from models.usuario import *
from flask_sqlalchemy import SQLAlchemy
from modules.db import db, app
#Importamos tokenizadores, separaran los reclamos en palabras clave para su posterior clasificación
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
#llevar palabras a palabras base
import spacy 
#Vectorizar palabras para procesar las similitudes
#from gensim.models.keyedvectors import KeyedVectors
#El modulo io se utiliza para abrir y manejar el archivo del modelo de palabras voctorizadas
#import io

#Instanciamos un objeto app de la calse Flask con el argumento __name__ que indica la ubicación del archivo 
#app = Flask(__name__)

app.secret_key="cvbnmrtyuiop"

"""app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_de_datos.db'

db = SQLAlchemy(app)
"""

#Crea laa base de datos 
with app.app_context():
    db.create_all()

"""

def load_vectors(archivo):
    fin = io.open(archivo, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

"""


#archivo = '/data/'
#data = load_vectors(archivo)



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
        print(vars(usuario))

        if usuario.tipo_usuario == "final" and usuario.check_password(contraseña):
            print("FINAL")  
            session['n_usuario'] = usuario.n_usuario
            session['nombre_usuario']=usuario.nombre_usuario
            session['contraseña']=usuario.contraseña
            session['nombre_de_pila']=usuario.nombre_de_pila
            session['edad']=usuario.edad
            session['claustro']=usuario.claustro
            session['correo']=usuario.correo
            session['tipo_usuario'] =usuario.tipo_usuario
            return redirect("/inicio")
        
        elif usuario.tipo_usuario == "jefe" and usuario.check_password(contraseña):
            #print("JEFE")
            #usuario = Jefe.query.filter_by(nombre_usuario=nombre_usuario).first()
            session['n_usuario'] = usuario.n_usuario
            session['nombre_usuario']=usuario.nombre_usuario
            session['contraseña']=usuario.contraseña
            session['nombre_de_pila']=usuario.nombre_de_pila
            session['edad']=usuario.edad
            session['correo']=usuario.correo
            session['tipo_usuario'] =usuario.tipo_usuario
            session['departamento']=usuario.departamento
            return redirect("/inicio")
        
        elif usuario.tipo_usuario == "secretario" and usuario.check_password(contraseña):
            #print("SECRETARIO")
            #usuario = Secretario.query.filter_by(nombre_usuario=nombre_usuario).first()
            session['n_usuario'] = usuario.n_usuario
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

@app.route("/crear_reclamo", methods=["GET","POST"])
def crear_reclamo():
    if request.method == "POST":
        try:
            usuario_id = session['n_usuario']
            asunto = request.form.get('asunto')
            texto = request.form.get('texto')
            new_reclamo = Reclamo(asunto, texto, usuario_id)
            todo_texto = asunto + ' ' + texto
            frases = sent_tokenize(todo_texto, language='spanish')
    
        # Descarga las stopwords de NLTK en español y crea un conjunto
            stop_words = set(stopwords.words('spanish'))

            # Elimina las stopwords de cada frase
            frases_filtradas = []
            nlp = spacy.load("es_core_news_sm")
            for frase in frases:
                #recorta las frases en palabras
                palabras = word_tokenize(frase, language='spanish')
                #filtra las palabras verificando que no sean stopwords
                palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stop_words]
                #concatena las palabras en una frase nueva
                frases_filtradas.append(' '.join(palabras_filtradas))

            # Lemaniza las palabras
            for frase in frases_filtradas:
                doc = nlp(frase)
                lemas = [token.lemma_ for token in doc]
                print(frase)
            
            dptos = Departamento.query.all()
            base=0
            print(dptos)
            for dpto in dptos:
                coincidencias = 0
                print(dpto)
                lista= dpto.keywords.split()
                
                for lema in lemas:
                    if lema in lista:
                        coincidencias = +1
                        print(coincidencias)
                    print(lema)
                if coincidencias > base: 
                    destino = dpto
                    base = coincidencias
            destino.asignar_reclamo(new_reclamo)

            db.session.add(new_reclamo)
            
            db.session.commit()

        except Exception:
           return render_template("/crear_reclamo.html")

        return redirect('/reclamos')
    else:
        return render_template("/crear_reclamo.html")


@app.route("/mis_reclamos", methods=["GET","POST"])
def mis_reclamos():
    bandera = "mis"
    return redirect("/reclamos")

@app.route("/listar_reclamos", methods=["GET","POST"])
def listar_reclamos():
    bandera = "listar"
    return redirect("/reclamos")

@app.route("/reclamos", methods=["GET","POST"])
def reclamos():
    if request.method == "POST":

        pass
        
    else:

        if bandera == "mis":
            reclamos = Reclamo.query.filter_by(creador_id=session['n_usuario']).all()

        elif bandera == "listar":
            reclamos = Reclamo.query.all()

        return render_template("/reclamos.html", reclamos=reclamos)

#Éstas líneas corren el programa de manera "continua"
if __name__ == "__main__":
    app.run(debug=True)
