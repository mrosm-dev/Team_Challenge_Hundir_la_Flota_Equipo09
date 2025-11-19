import numpy as np
import variables


class Tablero:
    def __init__(self, columnas, filas, usuario):
        self.usuario_id = usuario
        self.columnas = columnas
        self.filas = filas
        self.tablero = self.crear_tablero()

    def crear_tablero(self):
        return np.full((self.filas, self.columnas), variables.agua, dtype=str)

    def posicionar_barcos(self, barcos):
        for barco in barcos:
            for r, c in barco.coordenadas:
                self.tablero[r, c] = variables.barco
