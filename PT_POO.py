import random
import datetime

# ==============================
# FUNCIONES DEL JUEGO
# ==============================

def MostrarReglas():
    print("\n\t" + "="*26 + " REGLAS DEL JUEGO " + "="*26)
    print("\t1. El objetivo es llevar tu nave desde la Tierra (casillero 1) hasta Marte (casillero 50).")
    print("\t2. En cada turno lanzas un dado de 6 caras para avanzar.")
    print("\t3. Tipos de nave:")
    print("\t   - Exploradora: avanza +1 extra en cada turno.")
    print("\t   - De Carga: sobrevive una vez a un Campo de Asteroides.")
    print("\t4. Obstáculos del tablero (cada casilla activa el efecto solo una vez):")
    print("\t   * Agujero Negro (8–15): retrocede 5 casillas.")
    print("\t   * Campo de Asteroides (16–25): 50% de probabilidad de perder la nave.")
    print("\t   * Tormenta Solar (26–35): pierdes 2 turnos.")
    print("\t   * Falla de Motor (36–45): retrocedes al casillero 20.")
    print("\t5. Si pasas del casillero 50, rebota hacia atrás según lo que hayas avanzado.")
    print("\t6. Puedes abandonar la misión escribiendo 'S' durante tu turno.")
    print("\t" + "="*70 + "\n")


def RegistrarJugador(Jugador):
    while True:
        Nombre = input("\tIngrese nombre del jugador: ").strip()
        EsValido = True
        
        for Caracter in Nombre:
            if not (Caracter.isalpha() or Caracter.isspace()):
                EsValido = False
                break
        
        if EsValido and Nombre != "":
            Nombre = Nombre.capitalize()
            break
        else:
            print("\t! El nombre solo debe contener letras y espacios. Intente nuevamente.")
    
    while True:
        try:
            Edad = int(input("\tIngrese edad del jugador: "))
            if Edad >= 2 and Edad <= 90:
                break
            else:
                print("\t! Edad invalida. Intente nuevamente.")
        except ValueError:
            print("\t! Entrada inválida. Debe ingresar un número.")

    while True:
        TipoNave = input("\tSeleccione tipo de nave - [E]xploradora o [C]arga: ").upper()
        if TipoNave in ['E', 'C']:
            TipoNave = "Exploradora" if TipoNave == 'E' else "Carga"
            break
        else:
            print("\t! Opción inválida. Intente nuevamente.")
    
    Jugador = {
        "Nombre": Nombre,
        "Edad": Edad,
        "TipoNave": TipoNave,
        "Victorias": 0,
        "Derrotas": 0
    }
    
    print(f"\n\tJugador {Nombre} registrado exitosamente con nave {TipoNave}.\n")
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
        #Si debe saltar turnos
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
        if Posicion > 50:
            Rebote = Posicion - 50
            Posicion = 50 - Rebote
            print(f"\t¡Has rebotado en Marte y retrocedido a la posición {Posicion}!")
            
        if Posicion == 50:
            print(f"\t¡Has llegado a Marte en {Turnos} turnos!")
            Resultado = "Victoria"
            Jugador["Victorias"] += 1
            break

        # Obstáculos (solo una vez)
        if 8 <= Posicion <= 15 and "AgujeroNegro" not in ObstaculosActivados:
            Posicion -= 5
            ObstaculosActivados.add("AgujeroNegro")
            print(f"\tCayó en un Agujero Negro y retrocede a la posición {Posicion}.")

        elif 16 <= Posicion <= 25:
                if random.choice([True, False]):
                    if Jugador["TipoNave"] == "Carga" and SupervivenciaCarga:
                        SupervivenciaCarga = False
                        print("\tCampo de Asteroides dañado, pero tu nave de carga sobrevive.")
                    else:
                        print("\t¡Tu nave explotó en un Campo de Asteroides!")
                        Resultado = "Derrota"
                        Jugador["Derrotas"] += 1
                        break

        elif 26 <= Posicion <= 35 and "TormentaSolar" not in ObstaculosActivados:
            SaltarTurnos = 2
            ObstaculosActivados.add("TormentaSolar")
            print("\tTormenta Solar, pierdes los próximos 2 turnos.")

        elif 36 <= Posicion <= 45 and "FallaMotor" not in ObstaculosActivados:
            Posicion = 20
            ObstaculosActivados.add("FallaMotor")
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

    print("\n\t" + "="*31 + " ESTADÍSTICAS " + "="*31)
    print(f"\t{'Fecha':<22}{'Jugador':<15}{'Resultado':<15}{'Turnos':<10}{'Posición Final':<15}")
    print("\t" + "-" * 76)

    for Fecha, Datos in Historial.items():
        print(f"\t{Fecha:<22}{Datos['Nombre']:<15}{Datos['Resultado']:<15}{Datos['Turnos']:<10}{Datos['PosicionFinal']:<15}")

    print("\t" + "-" * 76)
    ReporteVictoriasDerrotas(Historial)
    ReportePromedioTurnos(Historial)


def ReporteVictoriasDerrotas(Historial):
    TotalVictorias = sum(1 for d in Historial.values() if d["Resultado"] == "Victoria")
    TotalDerrotas = sum(1 for d in Historial.values() if d["Resultado"] == "Derrota")
    
    print("\n\t===== REPORTE 1: VICTORIAS Y DERROTAS =====")
    print(f"\t{'Tipo':<20}{'Cantidad':<10}")
    print("\t" + "-"*30)
    print(f"\t{'Victorias':<20}{TotalVictorias:<10}")
    print(f"\t{'Derrotas':<20}{TotalDerrotas:<10}")
    print("\t" + "-"*30)


def ReportePromedioTurnos(Historial):
    if not Historial:
        print("\tNo hay partidas registradas.\n")
        return

    PromedioTurnos = sum(d["Turnos"] for d in Historial.values()) / len(Historial)

    print("\n\t" + "="*50)
    print("\t        REPORTE 2: PROMEDIO DE TURNOS")
    print("\t" + "="*50)
    print(f"\t{'Descripción':<35}{'Valor':<10}")
    print("\t" + "-"*50)
    print(f"\t{'Promedio de turnos por partida':<35}{PromedioTurnos:<10.2f}")
    print("\t" + "-"*50 + "\n")


# ==============================
# MENÚ PRINCIPAL
# ==============================

def Menu():
    Jugador = {}
    Historial = {}

    while True:
        print("\n\t" + "=" * 70)
        print("\t\t\t\t    MENÚ PRINCIPAL")
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
                Jugador = RegistrarJugador(Jugador)
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