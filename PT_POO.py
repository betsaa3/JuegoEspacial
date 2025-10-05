import random
import datetime

# ==============================
# FUNCIONES DEL JUEGO
# ==============================

def MostrarReglas():
    print("\n\t========== REGLAS DEL JUEGO ==========")
    print("\t1. El objetivo es llevar tu nave desde la Tierra (1) hasta Marte (50).")
    print("\t2. En cada turno lanzas un dado de 6 caras para avanzar.")
    print("\t3. Tipos de nave:")
    print("\t   - Exploradora: avanza +1 extra cada turno.")
    print("\t   - De Carga: sobrevive una vez a un campo de asteroides.")
    print("\t4. Obstáculos del tablero:")
    print("\t   * Agujero Negro (8–15): retrocede 5 casillas (una sola vez).")
    print("\t   * Campo de Asteroides (16–25): 50% de probabilidad de perder.")
    print("\t   * Tormenta Solar (26–35): pierdes 2 turnos (una sola vez).")
    print("\t   * Falla de Motor (36–45): retrocede al casillero 20 (una sola vez).")
    print("\t5. Si pasas del casillero 50, ganas automáticamente.")
    print("\t6. Puedes abandonar escribiendo 'S' durante tu turno.")
    print("\t=======================================\n")


def RegistrarJugador():
    Jugador = {}
    try:
        Nombre = input("\tIngrese nombre del jugador: ").capitalize()
        Edad = int(input("\tIngrese edad del jugador: "))
        while True:
            TipoNave = input("\tIngrese tipo de nave (Exploradora / Carga): ").capitalize()
            if TipoNave in ["Exploradora", "Carga"]:
                break
            else:
                print("\tTipo inválido. Intente nuevamente.")
        Jugador["Nombre"] = Nombre
        Jugador["Edad"] = Edad
        Jugador["TipoNave"] = TipoNave
        Jugador["Victorias"] = 0
        Jugador["Derrotas"] = 0
    except ValueError:
        print("\tEntrada inválida. Registro fallido.")
        return None
    return Jugador


def CrearTablero():
    Tablero = [i for i in range(1, 51)]
    return Tablero


def IniciarJuego(Jugador, Historial):
    if not Jugador:
        print("\tDebe registrar un jugador primero.")
        return

    Tablero = CrearTablero()
    Posicion = 1
    Turnos = 0
    SaltarTurnos = 0
    SupervivenciaCarga = True if Jugador["TipoNave"] == "Carga" else False
    ObstaculosActivados = set()  # guarda casillas ya activadas
    Resultado = ""

    while Posicion < 50:
        if SaltarTurnos > 0:
            print(f"\t{Jugador['Nombre']} pierde este turno por Tormenta Solar.")
            SaltarTurnos -= 1
            Turnos += 1
            continue

        Accion = input("\tPresione Enter para lanzar el dado o 'S' para abandonar: ").upper()
        if Accion == "S":
            print("\tHas abandonado la misión.")
            Resultado = "Abandono"
            break

        Dado = random.randint(1, 6)
        Avance = Dado
        if Jugador["TipoNave"] == "Exploradora":
            Avance += 1

        Posicion += Avance
        Turnos += 1
        print(f"\n\t{Jugador['Nombre']} lanzó {Dado} y avanzó {Avance} posiciones. Nueva posición: {Posicion}")

        # Llegada directa a Marte
        if Posicion >= 50:
            Posicion = 50
            print(f"\t¡Has llegado a Marte en {Turnos} turnos!")
            Resultado = "Victoria"
            Jugador["Victorias"] += 1
            break

        # Obstáculos (solo una vez por casilla)
        if 8 <= Posicion <= 15 and Posicion not in ObstaculosActivados:
            Posicion -= 5
            ObstaculosActivados.add(Posicion + 5)
            print(f"\tCayó en un Agujero Negro y retrocede a la posición {Posicion}.")

        elif 16 <= Posicion <= 25 and Posicion not in ObstaculosActivados:
            if random.choice([True, False]):
                if Jugador["TipoNave"] == "Carga" and SupervivenciaCarga:
                    SupervivenciaCarga = False
                    print("\tCampo de Asteroides dañado, pero tu nave de carga sobrevive.")
                else:
                    print("\t¡Tu nave explotó en un Campo de Asteroides!")
                    Resultado = "Derrota"
                    Jugador["Derrotas"] += 1
                    break
            ObstaculosActivados.add(Posicion)

        elif 26 <= Posicion <= 35 and Posicion not in ObstaculosActivados:
            SaltarTurnos = 2
            ObstaculosActivados.add(Posicion)
            print("\tTormenta Solar, pierdes los próximos 2 turnos.")

        elif 36 <= Posicion <= 45 and Posicion not in ObstaculosActivados:
            Posicion = 20
            ObstaculosActivados.add(Posicion)
            print("\tFalla de Motor, retrocedes a la posición 20.")

    # Guardar en historial
    Fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Historial[Fecha] = {
        "Nombre": Jugador["Nombre"],
        "Edad": Jugador["Edad"],
        "TipoNave": Jugador["TipoNave"],
        "Resultado": Resultado,
        "Turnos": Turnos,
        "PosicionFinal": Posicion
    }


def VerEstadisticas(Historial):
    if not Historial:
        print("\tNo hay juegos registrados todavía.\n")
        return

    print("\n\t=================== ESTADÍSTICAS ===================")
    print(f"\t{'Fecha':<22}{'Jugador':<15}{'Resultado':<15}{'Turnos':<10}{'Posición Final':<15}")
    print("\t" + "-" * 75)

    for Fecha, Datos in Historial.items():
        print(f"\t{Fecha:<22}{Datos['Nombre']:<15}{Datos['Resultado']:<15}{Datos['Turnos']:<10}{Datos['PosicionFinal']:<15}")

    print("\t" + "-" * 75)
    ReporteVictoriasDerrotas(Historial)
    ReportePromedioTurnos(Historial)


def ReporteVictoriasDerrotas(Historial):
    TotalVictorias = sum(1 for d in Historial.values() if d["Resultado"] == "Victoria")
    TotalDerrotas = sum(1 for d in Historial.values() if d["Resultado"] == "Derrota")
    print(f"\n\tReporte 1: Total de Victorias: {TotalVictorias} | Total de Derrotas: {TotalDerrotas}")


def ReportePromedioTurnos(Historial):
    PromedioTurnos = sum(d["Turnos"] for d in Historial.values()) / len(Historial)
    print(f"\tReporte 2: Promedio de turnos por partida: {PromedioTurnos:.2f}")
    print("\t=====================================================\n")


# ==============================
# MENÚ PRINCIPAL
# ==============================

def Menu():
    Jugador = {}
    Historial = {}

    while True:
        print("\n\t" + "=" * 70)
        print("\t\t\t    MENÚ PRINCIPAL")
        print("\t" + "=" * 70)
        print("\t[1] Instrucciones de cómo jugar")
        print("\t[2] Ingresar jugador")
        print("\t[3] Nuevo juego")
        print("\t[4] Ver estadísticas")
        print("\t[5] Salir")
        print("\t" + "=" * 70)

        try:
            Opcion = int(input("\tSeleccione una opción: "))
            
            if Opcion == 1:
                MostrarReglas()
            elif Opcion == 2:
                Jugador = RegistrarJugador()
            elif Opcion == 3:
                IniciarJuego(Jugador, Historial)
            elif Opcion == 4:
                VerEstadisticas(Historial)
            elif Opcion == 5:
                print("\n\tSaliendo del juego... ¡Hasta pronto!\n")
                break
            else:
                print("\tOpción inválida. Intente nuevamente.")
        except ValueError:
            print("\tEntrada inválida. Debe ingresar un número.")

if __name__ == "__main__":
    Menu() 