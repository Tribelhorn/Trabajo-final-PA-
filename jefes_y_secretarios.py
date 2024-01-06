from models.clases import Usuario
from models.db import db, app

Jefe1 = Usuario(nombre_usuario="JCarlos", correo="@Jefe1", contraseña="1234", nombre_de_pila="Juan Carlos Pavón", dni=int(44444447), edad=int(45), claustro="jefe")
Jefe2 = Usuario(nombre_usuario="Mariano", correo="@Jefe2", contraseña="1234", nombre_de_pila="Mariano Izaguirre", dni=int(44444448), edad=int(40), claustro="jefe")
Secretario = Usuario(nombre_usuario="Anibalito", correo="@Secre", contraseña="1234", nombre_de_pila="Anibal Sppindola", dni=int(44444443), edad=int(48), claustro="secretario")
with app.app_context():
    db.session.add(Jefe1)
    db.session.add(Secretario)
    db.session.add(Jefe2)
    db.session.commit()