from dataclasses import field
from typing import Dict, List, Optional, Tuple
import random
import variables

Coord = Tuple[int, int]  # (fila, columna), index empieza en 0

class Barco:
    def __init__(self, nombre: str, eslora: int):
        self.nombre: str = nombre
        self.eslora: int = eslora
        self.coordenadas: List[Coord] = []
        self.hits: List[bool] = []

    def fijar_coordenadas(self, coords: List[Coord]) -> None:
        self.coordenadas = list(coords) #asigna coordenadas
        self.hits = [False] * len(self.coordenadas) #iniciamos lista vacia

    def hundido(self) -> bool:
        return len(self.coordenadas) > 0 and all(self.hits)  #true si todas las posiciones del barco están impactadas y existen las coordenadas

    def vidas(self) -> int:
        return sum(1 for h in self.hits if not h) #nº casillas no impactadas, sanas

    def registrar_impacto(self, fila: int, col: int) -> bool:
        objetivo = (fila, col)
        for i, c in enumerate(self.coordenadas):
            if c == objetivo: #marca impacto si coordenadas corresponden a las del barco
                if not self.hits[i]:  # evita dar dos veces la misma casilla
                    self.hits[i] = True #devuelve true si ha sido impactado
                return True
        return False


class Barcos: #para gestionar todos los barcos de un jugador
#recibe el diccionario (nombre, eslora) os) y coloca todos los barcos dentro del tablero, sin solaparse
    def __init__(
        self,
        fleet_info: Dict[str, int],
        rows: int = variables.filas_tablero,
        cols: int = variables.columnas_tablero,
        seed: Optional[int] = None,
        max_intentos: int = 2000,
    ):
        self.rows = rows
        self.cols = cols
        self.fleet_info = dict(fleet_info)  # copia del diccionario para no modificar el original
        self.max_intentos = max_intentos
        self.rng = random.Random(seed)

        self.barcos: List[Barco] = [] #lista con barcos una vez colocados
        # creamos matriz booleana para saber si una casilla ya está ocupada por algún barco y evitar solapes
        self.ocupada: List[List[bool]] = [[False] * cols for _ in range(rows)]

        self.generar_coordenadas_n_barcos() #coloca la flota


    def generar_coordenadas_n_barcos(self):
    #colocamos los barcos de fleet_info
        self.barcos.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                self.ocupada[r][c] = False #limpiamos la matriz de ocupación, todo libre

        for nombre, eslora in sorted(self.fleet_info.items(), key=lambda kv: -kv[1]): #ordenamos por los mas grandes primero
            coords = self._generar_coordenadas_barco(eslora) #busca sitio válido para el barco
            barco = Barco(nombre=nombre, eslora=eslora) #crea el barco
            barco.fijar_coordenadas(coords) #inicia coordenadas
            self.barcos.append(barco)
            for (r, c) in coords:
                self.ocupada[r][c] = True #marca casillas ocupadas para que no sean usadas por otro barco

    def _generar_coordenadas_barco(self, eslora: int) -> List[Coord]:
        orientaciones = ["N", "S", "E", "O"]

        for _ in range(self.max_intentos):
            orient = self.rng.choice(orientaciones)
            fila = self.rng.randint(0, self.rows - 1)
            col = self.rng.randint(0, self.cols - 1)

            if orient == "N":
                coords = [(fila - i, col) for i in range(eslora)]
            elif orient == "S":
                coords = [(fila + i, col) for i in range(eslora)]
            elif orient == "E":
                coords = [(fila, col + i) for i in range(eslora)]
            else:  # "O"
                coords = [(fila, col - i) for i in range(eslora)]

            #para comprobar que estan dentro del tablero
            dentro = all(0 <= r < self.rows and 0 <= c < self.cols for r, c in coords)
            if not dentro:
                continue

            #para comprobar que estan libres las posiciones
            libre = all(not self.ocupada[r][c] for r, c in coords)
            if libre:
                return coords

        raise RuntimeError(
            f"No se pudo colocar un barco de eslora {eslora}, ha habido ya {self.max_intentos} intentos"
        )


    def registrar_impacto(self, fila: int, col: int) -> Optional[Barco]:
        for b in self.barcos:
            if b.registrar_impacto(fila, col):
                return b #devuelve true si fue impactado
        return None #devuelve none si fue al agua

    def vidas_totales(self) -> int:
        return sum(b.vidas() for b in self.barcos)

    def todos_hundidos(self) -> bool:
        return self.vidas_totales() == 0 #True si ya no queda ninguna casilla de barco viva.
