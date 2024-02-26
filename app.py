#Importamos la clase Flask, url_for sirve para redireccionar 
from flask import Flask, render_template, request, redirect, url_for, session, send_file
#from models.usuario_reclamo import *
from modules.clases import Usuario, Usuario_Final, Jefe, Secretario, Reclamo, adhesiones, Departamento 
#from models.usuario import *
from flask_sqlalchemy import SQLAlchemy
from db import db, app
#Importamos tokenizadores, separaran los reclamos en palabras clave para su posterior clasificación
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
#llevar palabras a palabras base
import spacy 
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import pdfkit
import jinja2
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
                #dni = int(request.form.get('dni'))
                edad = int(request.form.get('edad'))
                claustro = request.form.get('claustro')
                new_user = Usuario_Final(nombre_usuario=nombre_usuario, correo=correo, contraseña=contraseña, nombre_de_pila=nombre_de_pila, edad=edad, claustro=claustro)
            
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
        try:
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
                print("JEFE")
                #usuario = Jefe.query.filter_by(nombre_usuario=nombre_usuario).first()
                session['n_usuario'] = usuario.n_usuario
                session['nombre_usuario']=usuario.nombre_usuario
                session['contraseña']=usuario.contraseña
                session['nombre_de_pila']=usuario.nombre_de_pila
                session['edad']=usuario.edad
                session['correo']=usuario.correo
                session['tipo_usuario'] =usuario.tipo_usuario
                session['n_dpto']=usuario.n_dpto
                return redirect("/inicio")
            
            elif usuario.tipo_usuario == "secretario" and usuario.check_password(contraseña):
                print("SECRETARIO")
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
        except:
        #  print("No funca")
          render_template  ("/login.html")  
    return render_template("/login.html")        


@app.route("/inicio", methods=["GET","POST"])   
def inicio():
    try:
        session['mensaje'] = False
        if session['tipo_usuario'] == "final":
            print("Alooooooo")
            return render_template("inicio.html") #session["nombre_usuario"], session["nombre_de_pila"], session["edad"])
        elif session['tipo_usuario'] == "jefe":
            #print("ola k ase")
            return render_template("inicio_2.html")
        elif session['tipo_usuario'] == "secretario":
            return render_template("inicio_2.html")
        else:
            return redirect("/")
    except:
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/crear_reclamo", methods=["GET","POST"])
def crear_reclamo():
    if request.method == "POST":
        try:
            if 'imagen' in request.files:
                session['imagen']=request.files['imagen'].read() 
            usuario_id = session['n_usuario']
            asunto = request.form.get('asunto')
            texto = request.form.get('texto')
            #new_reclamo = Reclamo(asunto, texto, usuario_id)
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
            try: 
                dptos = Departamento.query.all()
                base=0
                print(dptos)
                for dpto in dptos:
                    print(dpto)
                    coincidencias = 0
                    print(dpto.keywords)
                    lista= dpto.keywords.split()
                    print(lista)
                    
                    for lema in lemas:
                        print("("+lema+")")
                        if lema in lista:
                            coincidencias = coincidencias +1
                    print(coincidencias)
                    if coincidencias > base: 
                        destino = dpto
                        base = coincidencias
                print(destino)
                
                session['bolsa'] = ' '.join(lemas)
                session['asunto'] = asunto
                session['texto'] = texto
                session['n_dpto'] = destino.n_dpto  
                
    
                return redirect("/confirmar")

            except:
                bolsa = ' '.join(lemas)
                new_reclamo = Reclamo(asunto, texto, usuario_id, bolsa)
                db.session.add(new_reclamo)
                if 'imagen' in session:
                    new_reclamo.añadir_imagen(session['imagen'])
                db.session.commit()
                session['mensaje'] = "Reclamo creado"
                return redirect('/mis_reclamos')

        except Exception:
            print("También un error")
            return render_template("/crear_reclamo.html")
            

    else:
        return render_template("/crear_reclamo.html")
    

@app.route("/confirmar", methods=["GET","POST"])
def confirmar():
    destino = Departamento.query.filter_by(n_dpto=session['n_dpto']).first()
    new_reclamo = Reclamo(session['asunto'], session['texto'], session['n_usuario'], session['bolsa'])
    reclamos=db.session.query(Reclamo).filter(Reclamo.creador_id != session['n_usuario'], Reclamo.n_dpto == session['n_dpto']).all()
    session['mensaje'] = False 
    if request.method == "POST":
        boton = request.form['boton']
        print(boton)
        if boton == "Confirmar reclamo":
            db.session.add(new_reclamo)
            destino.asignar_reclamo(new_reclamo)
            if 'imagen' in session:
                new_reclamo.añadir_imagen(session['imagen'])
            db.session.commit()
            session['mensaje'] = "Reclamo creado"
            return redirect("/mis_reclamos")
        else:
            reclamo = Reclamo.query.filter_by(codigo=boton).first()
            session['mensaje'] = reclamo.adherir(session['n_usuario'])
            return redirect("/listar_reclamos", mensaje=session['mensaje'])
    else:   
        return render_template("/confirmar.html", reclamos=reclamos) 


@app.route("/mis_reclamos", methods=["GET","POST"])
def mis_reclamos():
    if 'mensaje' in session:
        mensaje = session['mensaje']
    else:
        mensaje= False
    departamentos = Departamento.query.all()
    reclamos = Reclamo.query.filter_by(creador_id=session['n_usuario']).all()
    if request.method == "POST":
        if 'departamento' in request.form:
            dpto = request.form['departamento']
            reclamos = Reclamo.query.filter_by(n_dpto=dpto, creador_id=session['n_usuario']).all()
        
        return render_template("/mis_reclamos.html", reclamos=reclamos, departamentos=departamentos, mensaje=mensaje)
    return render_template("/mis_reclamos.html", reclamos=reclamos, departamentos=departamentos, mensaje=mensaje)

@app.route("/listar_reclamos", methods=["GET","POST"])
def listar_reclamos():
    departamentos = Departamento.query.all()
    reclamos = Reclamo.query.all()
    if 'mensaje' in session:
        mensaje = session['mensaje']
    else:
        mensaje= False
    if request.method == "POST":
        if 'departamento' in request.form:
            dpto = request.form['departamento']
            reclamos = Reclamo.query.filter_by(n_dpto=dpto).all()
        elif 'boton' in request.form:
            boton = request.form['boton']
            reclamo_adhesion = Reclamo.query.filter_by(codigo=boton).first()
            mensaje = reclamo_adhesion.adherir(session['n_usuario'])
            reclamos = Reclamo.query.all()
        return render_template("/listar_reclamos.html", reclamos=reclamos, departamentos=departamentos, mensaje=mensaje)
    return render_template("/listar_reclamos.html", reclamos=reclamos, departamentos=departamentos, mensaje=mensaje)

@app.route("/analitica", methods=["GET","POST"])
def analitica():
    if session['tipo_usuario'] == "jefe":
        #departamentos = Departamento.query.filter_by(n_dpto = session['n_dpto']).first()
        reclamos = Reclamo.query.filter_by(n_dpto = session['n_dpto']).all()
        print(session['n_dpto']) 
    elif session['tipo_usuario'] == "secretario":
        reclamos = Reclamo.query.all()
        #departamentos=Departamento.query.all()
    pendientes = 0
    invalidos = 0
    en_proceso = 0
    resueltos = 0
    for reclamo in reclamos:

        if reclamo.estado == "Pendiente":
            pendientes = pendientes +1
        elif reclamo.estado =="Inválido":
            invalidos = invalidos +1
        elif reclamo.estado == "En proceso":
            en_proceso = en_proceso +1
        elif reclamo.estado == "Resuelto":
            resueltos = resueltos +1
    
    total = len(reclamos)
    
    if total == 0:
        pass
    else:
        porcentajes = [((pendientes*100)/total), ((invalidos*100)/total), ((en_proceso*100)/total), ((resueltos*100)/total)]
        etiquetas = ["Pendientes", "Invalidos", "En proceso", "Resueltos"]

        #evita que haya valores nulos en el gáfico
        
        porcentajes_no_nulo = [porcentaje for porcentaje in porcentajes if porcentaje != 0]
        etiquetas_no_nulo = [etiqueta for i, etiqueta in enumerate(etiquetas) if porcentajes[i] != 0]

        print(porcentajes_no_nulo)

        plt.figure(figsize=(6, 6))  # Tamaño de la figura
        plt.pie(porcentajes_no_nulo, labels=etiquetas_no_nulo, autopct='%1.1f%%', startangle=140) 
        plt.axis('equal') 
        plt.title('Estado de los reclamos')
        plt.savefig('static/grafico_torta.png')

    palabras = ""
    for reclamo in reclamos:
        palabras= palabras + " " + reclamo.bolsa
    
   
    # Generar la nube de palabras
    wordcloud = WordCloud(width=500, height=500, background_color='white').generate(palabras)

    # Mostrar la nube de palabras
    plt.figure(figsize=(6, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Palabras más fracuentes')
    plt.savefig('static/top_palabras.png')


    return render_template("/analitica.html")

@app.route("/manejar", methods=["GET","POST"])
def manejar():
    tipo_usuario=session['tipo_usuario']
    if session['tipo_usuario'] == "jefe":
        departamentos = Departamento.query.filter_by(n_dpto = session['n_dpto']).first()
        reclamos = Reclamo.query.filter_by(n_dpto = session['n_dpto']).all()
        print(session['n_dpto']) 
    elif session['tipo_usuario'] == "secretario":
        reclamos = Reclamo.query.all()
        departamentos=Departamento.query.all()
    else:
        pass
    if request.method == "POST":
        if 'departamento' in request.form:
            dpto= request.form['departamento']
            print("dpto")
            codigo= request.form['boton']
            departamento = Departamento.query.filter_by(n_dpto=dpto).first()
            reclamo = Reclamo.query.filter_by(codigo=codigo).first()
            departamento.asignar_reclamo(reclamo)
            db.session.commit()
        elif 'estado' in request.form:
            estado = request.form['estado']
            codigo = request.form['boton']
            reclamo = Reclamo.query.filter_by(codigo=codigo).first()
            reclamo.cambiar_estado(estado)
            db.session.commit()
        else:
            pass
         
        
    return render_template("/manejar.html", reclamos=reclamos, departamentos=departamentos, tipo_usuario=tipo_usuario)


@app.route("/help", methods=["GET","POST"])
def help():
    return render_template("/help.html")

@app.route("/reporte", methods=["GET","POST"])
def reporte():
    if request.method == 'POST':
        print(request.form)
        if session['tipo_usuario'] == "jefe":
            #departamentos = Departamento.query.filter_by(n_dpto = session['n_dpto']).first()
            reclamos = Reclamo.query.filter_by(n_dpto = session['n_dpto']).all()
            print(session['n_dpto']) 
        elif session['tipo_usuario'] == "secretario":
            reclamos = Reclamo.query.all()
            #departamentos=Departamento.query.all()
        
            
        pendientes = 0
        invalidos = 0
        en_proceso = 0
        resueltos = 0
        for reclamo in reclamos:

            if reclamo.estado == "Pendiente":
                pendientes = pendientes +1
            elif reclamo.estado =="Inválido":
                invalidos = invalidos +1
            elif reclamo.estado == "En proceso":
                en_proceso = en_proceso +1
            elif reclamo.estado == "Resuelto":
                resueltos = resueltos +1
            
        total = len(reclamos)
            
        if total == 0:
            pass
        else:
            porcentajes = [((pendientes*100)/total), ((invalidos*100)/total), ((en_proceso*100)/total), ((resueltos*100)/total)]
            etiquetas = ["Pendientes", "Invalidos", "En proceso", "Resueltos"]

            #evita que haya valores nulos en el gáfico
                
            porcentajes_no_nulo = [porcentaje for porcentaje in porcentajes if porcentaje != 0]
            etiquetas_no_nulo = [etiqueta for i, etiqueta in enumerate(etiquetas) if porcentajes[i] != 0]

            print(porcentajes_no_nulo)
            plt.figure(figsize=(6, 6))  # Tamaño de la figura
            plt.pie(porcentajes_no_nulo, labels=etiquetas_no_nulo, autopct='%1.1f%%', startangle=140) 
            plt.axis('equal') 
            plt.title('Estado de los reclamos')
            plt.savefig('static/grafico_torta.png')
        plantilla = render_template("/reporte.html", reclamos=reclamos)
        if request.form['reporte'] == "HTML":
            
            return plantilla
        elif request.form['reporte'] == "PDF":
            #pdfkit.from_string()
            options = {'enable-local-file-access': None , 'encoding': 'utf-8'}
            nueva_ruta =  r"C:\Users\Usuario\Desktop\Bioing\2do\PAvanzada\FINAL\Trabajo-final-PA-\static\grafico_torta.png"
            plantilla = plantilla.replace("/static/grafico_torta.png", nueva_ruta)
            pdfkit.from_string(plantilla,'reporte.pdf', configuration=pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"), options=options)
            return send_file('reporte.pdf', as_attachment=True)

        else:
            return redirect("/inicio")

#Éstas líneas corren el programa de manera "continua"
if __name__ == "__main__":
    app.run(debug=True)

