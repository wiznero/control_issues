import sqlite3
from Clases_jugador import Jugador  # Asegúrate de que jugador.py esté en la misma carpeta

# Crear base temporal de prueba
conn = sqlite3.connect("test_jugadores.db")
cursor = conn.cursor()

# Crear tabla (si no existe)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS jugadores (
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
conn.commit()

# Crear jugador de prueba
jugador = Jugador("12345678A", "Sergio", "Gil", 28)

# Insertarlo manualmente en la base de datos
cursor.execute("""
    INSERT OR REPLACE INTO jugadores (dni, nombre, apellido, edad, saldo)
    VALUES (?, ?, ?, ?, ?)
""", (jugador.dni, jugador.nombre, jugador.apellido, jugador.edad, jugador.saldo))
conn.commit()

print("\n🧪 Test: Apostar 100 €")
jugador.apostar(100, conn)

print("\n🧪 Test: Ganar 200 € en slots")
jugador.ganar(200, "slots", conn)

print("\n🧪 Test: Perder 50 € en ruleta")
jugador.perder(50, "ruleta", conn)

print("\n🧪 Test: Retirar 300 €")
jugador.retirar(300, conn)

print("\n🧪 Test: Depositar 500 €")
jugador.depositar(500, conn)

print("\n🧪 Test: Mostrar perfil")
jugador.mostrar_perfil()

print("\n🧪 Test finalizado")
