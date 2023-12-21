import sqlite3

# Conectar a la base de datos (creará el archivo si no existe)
conn = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Ejemplo: Crear una tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        email TEXT
    )
''')

# Guardar los cambios
conn.commit()

cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", ('Juan Pérez', 'juan@email.com'))
conn.commit()

# Leer todos los usuarios
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()
print(usuarios)

# Actualizar un usuario
cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", ('Juan González', 1))
conn.commit()

# Eliminar un usuario
#cursor.execute("DELETE FROM usuarios WHERE id = ?", (1,))
#conn.commit()