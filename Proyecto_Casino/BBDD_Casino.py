import sqlite3

def crear_base_y_tabla():
    # 1. Conectar a la base de datos (se crea si no existe)
    conexion = sqlite3.connect("casino.db")
    cursor = conexion.cursor()

    # 2. Crear tabla de jugadores (solo si no existe)
    cursor.execute("""CREATE TABLE IF NOT EXISTS jugadores (
        dni TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        edad INTEGER NOT NULL,
        saldo REAL DEFAULT 1000,
        total_ganado REAL DEFAULT 0,
        total_perdido REAL DEFAULT 0,
        partidas_jugadas INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1
       )
    """)

    # 3. Guardar cambios y cerrar conexión
    conexion.commit()
    conexion.close()
    print("✅ Tabla 'jugadores' creada o ya existía.")

# Llamar a la función
crear_base_y_tabla()
input("Presiona Enter para continuar...")

# Función para actualizar el saldo de un jugador
def actualizar_saldo(dni, nuevo_saldo, conn):
    conn.execute("UPDATE jugadores SET saldo = ? WHERE dni = ?", (nuevo_saldo, dni))
    conn.commit()

# Función para actualizar el nivel, partidas y pérdidas
def actualizar_nivel_y_perdidas(dni, nivel, total_perdido, partidas, conn):
    conn.execute("UPDATE jugadores SET nivel = ?, total_perdido = ?, partidas_jugadas = ? WHERE dni = ?", (nivel, total_perdido, partidas, dni))
    conn.commit()

# Función para obtener datos de un jugador (saldo y nivel, por ejemplo)
def obtener_datos_jugador(dni, conn):
    cursor = conn.execute("SELECT saldo, nivel FROM jugadores WHERE dni = ?", (dni,))
    return cursor.fetchone()

# Función para guardar saldo y nivel al cerrar sesión
def cerrar_sesion(dni, saldo, nivel, conn):
    conn.execute("UPDATE jugadores SET saldo = ?, nivel = ? WHERE dni = ?", (saldo, nivel, dni))
    conn.commit()


