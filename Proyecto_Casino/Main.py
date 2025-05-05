# Main
# modulos de python
import sqlite3
from Clases_jugador import Jugador

# modulos de rich
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Conectar a la BD (se crea si no existe)
conn = sqlite3.connect("casino.db")
cursor = conn.cursor()