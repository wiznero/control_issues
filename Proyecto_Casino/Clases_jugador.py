# Clases para el proyecto
# importamos las librerias de rich
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import sqlite3
from BBDD_Casino import actualizar_saldo, actualizar_nivel_y_perdidas, obtener_datos_jugador, cerrar_sesion


# Inicializar la consola de rich para mejorar la presentación
console = Console()

# clase jugador----------------------------------------------------------------------------------------------------------
class Jugador:
    # Constructor de la clase jugador
    def __init__(self, dni, nombre, apellido, edad, saldo=1000):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.saldo = saldo
        self.historial = [] # Lista de ganancias y perdidas
        self.total_ganado = 0
        self.total_perdido = 0
        self.partidas_jugadas = 0
        self.nivel = 1
        self.activo = False # Para saber si está logueado
                   

# Metodos de la clase jugador----------------------------------------------------------------------------------

    # Metodo para apostar-----------------------------------------------------
    def apostar(self, cantidad, conn):
        #Resta saldo al jugador si tiene suficiente.
        if self.saldo >= cantidad and cantidad > 0:
            self.saldo -= cantidad
            actualizar_saldo(self.dni, self.saldo, conn)
            self.historial.append(f"Apuesta de {cantidad} € realizada")
            # actualizamos el nivel del jugador si es necesario
            console.print(f"[green]✓ Apuesta realizada: {cantidad} €[/green]")
            return True
        else:
             console.print("[red]✘ Error: Saldo insuficiente o cantidad no válida[/red]")
             return False
    
          
    # Metodo para ganar dinero-----------------------------------------------------
    def ganar(self, cantidad, juego, conn):
        # Suma saldo al jugador.
        if cantidad > 0:
            self.saldo += cantidad
            actualizar_saldo(self.dni, self.saldo, conn)
            self.historial.append(f"Has ganado {cantidad} € en {juego}")
            self.total_ganado += cantidad
            self.partidas_jugadas += 1
            console.print(f"[bold gold]🎉 ¡Ganaste {cantidad} € en {juego}![/bold gold]")
        else:
            console.print("[red]Error: Cantidad inválida[/red]")

    
    def perder(self, cantidad, juego, conn):
        if cantidad > 0:
            if cantidad <= self.saldo:
                self.saldo -= cantidad
                self.total_perdido += cantidad
                self.historial.append(f"Perdió {cantidad} € en {juego}")
                self.partidas_jugadas += 1
                actualizar_saldo(self.dni, self.saldo, conn)
                
            else:
                console.print("[red]Error: Saldo insuficiente[/red]")
        else:
            console.print("[red]Error: Cantidad invalida[/red]")

        console.print(f"[red]✘ Has perdido {cantidad} € en {juego}[/red]")

          
    # Metodo para retirar dinero---------------------------------------------------------------
    def retirar(self, cantidad, conn):
        # validamos que la cantidad sea superior a 0
        if cantidad <= 0:
            console.print("[bold red]✘ Error: Cantidad no válida[/bold red]")
            return False
        # validamos que el saldo sea superior a la cantidad a retirar 
        if self.saldo < cantidad:
            console.print("[bold red]✘ Error: Saldo insuficiente[/bold red]")
            return False
        #si cumple las condiciones, se retira el dinero
        self.saldo -= cantidad
        actualizar_saldo(self.dni, self.saldo, conn)
        self.historial.append(f"Retiro de {cantidad} €")
        console.print(f"[green]✓ Retiro realizado: {cantidad} €[/green]")
        return True
        
    
    # Metodo para depositar dinero en el saldo----------------------------------------------------
    def depositar(self, cantidad, conn):
        # Añade dinero al saldo del jugador
        if cantidad > 0:
            self.saldo += cantidad
            actualizar_saldo(self.dni, self.saldo, conn)
            self.historial.append(f"Deposito de {cantidad} € realizada")
            console.print(f"[green]✓ Deposito realizado: {cantidad} €[/green]")
            return True
        else:
            console.print("[red]✘ Error: Cantidad no válida, ingrese una cantidad superior a 0 [/red]")
            return False
        
    # Metodo para mostrar el saldo--------------------------------------------------------------------------
    def mostrar_saldo(self):
        console.print(f"[bold gold]Saldo actual: {self.saldo} €[/bold gold]")
        if self.saldo > 0:
            console.print("[green]¡Aún puedes hacerte millonario![/green]")
        else:
            console.print("[red]¿Seguro que no tienes algo que vender?[/red]")
        input("Presiona Enter para volver")
        
    # Metodo para actualizar nivel----------------------------------------------------------------------------
    def actualizar_nivel(self, conn):
        nivel_anterior = self.nivel
        self.nivel = 1 + (self.partidas_jugadas // 10)  # Cada 10 partidas = +1 nivel (base)
    
        # Bonificación cada 5 niveles (niveles 5, 10, 15...)
        if self.nivel > nivel_anterior and self.nivel % 5 == 0:  # Si sube de nivel Y es múltiplo de 5
            bonificacion = self.nivel * 50  # Ejemplo: 50 € por cada 5 niveles
            self.saldo += bonificacion
            actualizar_nivel_y_perdidas(self.dni,self.nivel, self.total_perdido, self.partidas_jugadas, conn)
            console.print(f"[bold gold]🎊 ¡Bonus de nivel {self.nivel}! +{bonificacion} €[/bold gold]")
        elif self.nivel > nivel_anterior:
            console.print(f"[green]↑ Subiste al nivel {self.nivel}[/green]")




    # Metodo para logearse-------------------------------------------------------------------------------------
    def login(self, conn):
        if not self.activo:
            # Cargar datos actualizados desde la BD
            datos = obtener_datos_jugador(self.dni, conn)  # Asignar el resultado a 'datos'
            
            if not datos:  # Si no existe el DNI
                console.print("[bold red]✘ Error: DNI no registrado. Regístrate primero.[/bold red]")
                return False  # Login fallido

            # Si existe, actualizar atributos y loguear
            self.saldo, self.nivel = datos
            self.activo = True
            console.print(f"[bold green] ¡Bienvenido/a, {self.nombre}![/bold green]")
            return True
        else:
            console.print("[bold yellow] Ya estabas logueado.[/bold yellow]")
            return False

        

    # Metodo para desconectarse---------------------------------------------------------------------------------
    def logout(self,conn):
        if self.activo:
            self.activo = False
            cerrar_sesion(self.dni, self.saldo, self.nivel, conn)
            console.print(f"[bold blue]🔒 Sesión cerrada. ¡Hasta pronto, {self.nombre}![/bold blue]")
            return True
        else:
            console.print("[bold yellow]⚠ No hay una sesión activa.[/bold yellow]")
            return False
        # Marcar al jugador como inactivo.

    def mostrar_perfil(self):
        # Devuelve un resumen del jugador: nombre, nivel, saldo, etc.
        tabla_perfiles = Table(title="Perfil Del Jugador", box=box.SIMPLE)
        tabla_perfiles.add_column("Campo", style="cyan")
        tabla_perfiles.add_column("valor", style="white")
        tabla_perfiles.add_row("Nombre", self.nombre)
        tabla_perfiles.add_row("Apellido", self.apellido)
        tabla_perfiles.add_row("DNI", self.dni)
        tabla_perfiles.add_row("Edad", str(self.edad))
        tabla_perfiles.add_row("saldo", str(self.saldo) + " €")
        tabla_perfiles.add_row("Nivel", str(self.nivel))
        tabla_perfiles.add_row("Partidas Jugadas", str(self.partidas_jugadas))
        tabla_perfiles.add_row("Total Ganado", str(self.total_ganado) + " €")
        tabla_perfiles.add_row("Total Perdido", str(self.total_perdido) + " €")
        tabla_perfiles.add_row("Historial", str(self.historial))
        console.print(Panel(tabla_perfiles, border_style="blue"))
        console.print("[green]¡Gracias por jugar con nosotros![/green]")
        input("Presiona Enter para volver al menu principal")

        

# fin de la clase jugador---------------------------------------------------------------------------------------------------------
