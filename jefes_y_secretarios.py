from modules.clases import Departamento, Secretario, Jefe
from db import db , app

academica = Departamento("Academica")
extension = Departamento("Extensión")
print(academica.n_dpto)
with app.app_context():
    db.session.add(academica)
    db.session.add(extension)
    db.session.commit()
    academica=Departamento.query.filter_by(nombre_dpto="Academica").first()
    extension=Departamento.query.filter_by(nombre_dpto="Extensión").first()

print(academica.n_dpto)


secretario = Secretario("Baldu", "Correo@Balducci_Fer.com", "1234", "Fernando Balducci", "45")
jefe1 = Jefe("Naudios", "Correo@Andre_Nau.com", "1234" ,"Andrés Naudi", "50",  academica)
jefe2 = Jefe("Greatel", "Correo@Gretel_Ram.com", "1234" , "Gretel Ramirez", "47" , extension)

academica.cargar_keywords(" inscripción materia calendario académico evaluacion exámen solicitud certificado cambio carrera programa estudio tutoría académica reglamento requisito graduación problema profesor")
extension.cargar_keywords(" actividad extracurricular evento conferencia programa voluntariado práctica profesional oportunidad intercambio servicio comunitario oferta curso taller proyecto extensión beca ayuda económica")

with app.app_context():
    db.session.add(academica)
    db.session.add(extension)
    db.session.add(secretario)
    db.session.add(jefe1)
    db.session.add(jefe2)    
    db.session.commit()

