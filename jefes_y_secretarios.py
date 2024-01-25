from modules.clases import Departamento, Secretario, Jefe
from modules.db import db , app

alumnado = Departamento("Alumnado")
ordenanzas = Departamento("Ordenanza")

secretario = Secretario("Sergio_D", "@Dervie_S", "1234", "Sergio Dervie", "44444445", "45")
jefe1 = Jefe("Juanjo_C", "@Copola_JJ", "1234" ,"Juan José Copola", "44444446", "50",  alumnado)
jefe2 = Jefe("NicolasD", "@Nicki_Dem", "1234" , "Nicolas Demel","44444447", "37" , ordenanzas)
with app.app_context():
    db.session.add(alumnado)
    db.session.add(ordenanzas)
    db.session.add(secretario)
    db.session.add(jefe1)
    db.session.add(jefe2)
    db.session.commit()