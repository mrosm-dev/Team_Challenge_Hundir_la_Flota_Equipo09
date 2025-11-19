from clases.tablero import Tablero
from clases.barco import Barcos
import modulo_funciones as mf
import variables


def init():
    tablero_jugador = Tablero(variables.columnas_tablero, variables.filas_tablero, 0)
    tablero_IA = Tablero(variables.columnas_tablero, variables.filas_tablero, 1)

    barcos_jugador = Barcos(variables.flota)
    barcos_IA = Barcos(variables.flota)

    tablero_jugador.posicionar_barcos(barcos_jugador.barcos)
    tablero_IA.posicionar_barcos(barcos_IA.barcos)

    return tablero_jugador, tablero_IA, barcos_jugador, barcos_IA


def update(tab_jug, tab_ia, bar_jug, bar_ia):

    jugador_turno = True

    while True:

        print("\n---- TU TABLERO ----") # TODO TABLERO JUGADOR
        print(tab_jug.tablero)

        print("\n ---TABLERO DE LA IA ---")
        mf.mostrar_tablero_visible_IA(tab_ia.tablero)

        if jugador_turno:
            print("\n--- TU TURNO ---") # TURNO JUGADOR
            sigue = mf.disparoJugador(tab_ia.tablero, bar_ia)

            if bar_ia.todos_hundidos():
                print("\nHAS GANADO!")
                break

            if not sigue:
                jugador_turno = False

        else:
            print("\n--- TURNO DE LA IA ---")
            mf.disparoIA(tab_jug.tablero, bar_jug)
            

            if bar_jug.todos_hundidos():
                print("\nLa IA te ha ganado...")
                break

            jugador_turno = True


def end():
    print("\nGracias por jugar.\n")


def main():
    tab_jug, tab_ia, bar_jug, bar_ia = init()
    update(tab_jug, tab_ia, bar_jug, bar_ia)
    end()


main()
