from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_url_path='/static', template_folder=os.path.abspath('templates')) #Indica la ruta a templates independientamente del directorio
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base_datos.db' 
db = SQLAlchemy(app)

