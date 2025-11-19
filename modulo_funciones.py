import numpy as np
import random
import variables


def mostrar_tablero_visible_IA(tablero_real):
    visible = np.full(tablero_real.shape, " ", dtype=str)

    for r in range(tablero_real.shape[0]):
        for c in range(tablero_real.shape[1]):
            casilla = tablero_real[r, c]

            if casilla == variables.tocado:
                visible[r, c] = variables.tocado
            elif casilla == variables.agua_tiro:
                visible[r, c] = variables.agua_tiro

    print(visible)


def disparoJugador(tablero_IA, barcos_IA):

    while True:
        coords = input("Introduce coordenadas (fila,col): ")

        if "," not in coords:
            print("Formato incorrecto")
            continue

        fila, col = coords.split(",")

        if not fila.isdigit() or not col.isdigit():
            print("Deben ser números")
            continue

        fila = int(fila)
        col = int(col)

        if not (0 <= fila < variables.filas_tablero and 0 <= col < variables.columnas_tablero):
            print("Coordenadas fuera del tablero")
            continue

        break

    barco = barcos_IA.registrar_impacto(fila, col)

    if barco:
        tablero_IA[fila, col] = variables.tocado
        print("Tocado!")
        if barco.hundido():
            print(f"Hundido: {barco.nombre}")
        return True  # sigue disparando

    else:
        tablero_IA[fila, col] = variables.agua_tiro
        print("Agua")
        return False   # pasa turno


coordenadas_usadas_IA = set()

def disparoIA(tablero_jugador, barcos_jugador):

    while True:
        fila = random.randint(0, variables.filas_tablero - 1)
        col = random.randint(0, variables.columnas_tablero - 1)

        if (fila, col) not in coordenadas_usadas_IA:
            coordenadas_usadas_IA.add((fila, col))
            break

    print(f"La IA dispara a ({fila},{col})")

    barco = barcos_jugador.registrar_impacto(fila, col)

    if barco:
        tablero_jugador[fila, col] = variables.tocado
        print("La IA te ha dado")
        if barco.hundido():
            print(f"La IA hundió tu {barco.nombre}")
    else:
        tablero_jugador[fila, col] = variables.agua_tiro
        print("La IA hizo agua")
