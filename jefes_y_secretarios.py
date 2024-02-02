from modules.clases import Departamento, Secretario, Jefe
from modules.db import db , app

academica = Departamento("Academica")
extension = Departamento("Extensión")

secretario = Secretario("Baldu", "@Balducci_Fer", "1234", "Fernando Balducci", "44444445", "45")
jefe1 = Jefe("Naudios", "@Andre_Nau", "1234" ,"Andrés Naudi", "44444446", "50",  academica)
jefe2 = Jefe("Greatel", "@Gretel_Ram", "1234" , "Gretel Ramirez","44444447", "47" , extension)

academica.cargar_keywords(" inscripción materia calendario académico evaluacion exámen solicitud certificado cambio carrera programa estudio tutoría académica reglamento requisito graduación problema profesor")
extension.cargar_keywords(" actividad extracurricular evento conferencia programa voluntariado práctica profesional oportunidad intercambio servicio comunitario oferta curso taller proyecto extensión beca ayuda económica")

with app.app_context():
    db.session.add(academica)
    db.session.add(extension)
    db.session.add(secretario)
    db.session.add(jefe1)
    db.session.add(jefe2)
    db.session.commit()

