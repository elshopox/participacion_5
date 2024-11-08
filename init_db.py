import sqlite3

# Conectar o crear la base de datos `almacen.db`
conn = sqlite3.connect('almacen.db')
cursor = conn.cursor()

# Crear la tabla `producto` si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)
''')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos 'almacen.db' y tabla 'producto' creadas exitosamente.")
