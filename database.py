import sqlite3

conn = sqlite3.connect('GestRest.db')
c = conn.cursor()

# Intentar seleccionar datos de la tabla.
try:
    c.execute('SELECT * FROM usuarios')
    print("La tabla 'usuarios' existe.")
except sqlite3.OperationalError:
    print("La tabla 'usuarios' no existe.")

conn.close()

