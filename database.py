import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('GestRest.db')
c = conn.cursor()

# Crear tabla de restaurantes
c.execute('''
    CREATE TABLE restaurantes (
        id_restaurante INTEGER PRIMARY KEY,
        nombre TEXT
    )
''')

# Crear tabla de productos
c.execute('''
    CREATE TABLE productos (
        id_producto INTEGER PRIMARY KEY,
        nombre TEXT,
        categoria TEXT  -- categorias: Cocina, Limpieza, Barra
    )
''')

# Crear tabla de usuarios
c.execute('''
    CREATE TABLE usuarios (
        id_usuario INTEGER PRIMARY KEY,
        nombre TEXT,
        rol TEXT,  -- roles: cocina, barra, limpieza, administrador
        id_restaurante INTEGER,
        FOREIGN KEY(id_restaurante) REFERENCES restaurantes(id_restaurante)
    )
''')

# Guardar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

