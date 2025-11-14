from dataclasses import field
rom typing import Dict, List, Optional, Tuple
import random

Coord = Tuple[int, int]  # (fila, columna), empezando en 0

class Barco:
    nombre: str
    eslora: int #cuantas casillas ocupa, la longitud del barco
    coordenadas: List[Coord] = field(default_factory=list) #genera lista vacia para cada barco
    hits: List[bool] = field(default_factory=list) # marca true si la casilla del barco es impactada

    def fijar_coordenadas(self, coords):
        self.coordenadas = list(coords) #asignamos coordenadas barco
        self.hits = [False] * len(self.coordenadas) #lista de impactos mismo tamaño que coordenadas, al principio la marcamos toda con false porque asumimos que no hay impactos

    def hundido(self):
        return len(self.coordenadas) > 0 and all(self.hits) #si todas las posiciones están impactadas y existen coordenadas, el barco está hundido
        #devuelve true si está hundido

    def vidas(self) -> int:
        return sum(1 for h in self.hits if not h) #recorremos hits y sumamos las que son False (no impactadas)

    def registrar_impacto(self, fila, col):
    # si las coordenadas pertenecen al barco, marca el impacto y devuelve True.
        objetivo = (fila, col)
        for i, c in enumerate(self.coordenadas):
            if c == objetivo:
                if not self.hits[i]:  # por si disparan dos veces a la misma
                    self.hits[i] = True
                return True
        return False

class Barcos: #para gestionar todos los barcos de un jugador
#recibe el diccionario (nombre, eslora) os) y coloca todos los barcos dentro del tablero, sin solaparse
    def __init__(
        self,
        fleet_info: Dict[str, int],
        rows: int = filas_tablero,
        cols: int = columnas_tablero,
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
        orientaciones = [(1, 0), (0, 1)]  # vertical (1,0) y horizontal (0,1)

        for _ in range(self.max_intentos):
            dr, dc = self.rng.choice(orientaciones) #orientacion aleatoria

            max_fila = self.rows - (eslora if dr == 1 else 1) #Si es vertical (dr==1), resta eslora a filas.
            max_col = self.cols - (eslora if dc == 1 else 1) #Si es horizontal (dc==1), resta eslora a columnas.
            fila = self.rng.randint(0, max_fila)
            col = self.rng.randint(0, max_col)

            coords = [(fila + i * dr, col + i * dc) for i in range(eslora)] #Construye todas las casillas que ocuparía el barco

            if all(not self.ocupada[r][c] for (r, c) in coords): #Si todas esas casillas están libres (False en ocupada), devuelve esas coordenadas
                return coords

        raise RuntimeError(
            f"No se pudo colocar un barco de eslora {eslora} tras {self.max_intentos} intentos"
        )

    def registrar_impacto(self, fila: int, col: int) -> Optional[Barco]:
        for b in self.barcos:
            if b.registrar_impacto(fila, col):
                return b #devuelve true si fue impactado
        return None #devuelve none si fue al agua

    def vidas_totales(self) -> int:
        return sum(b.vidas for b in self.barcos) #Suma las vidas (casillas no impactadas) de todos los barcos

    def todos_hundidos(self) -> bool:
        return self.vidas_totales() == 0 #True si ya no queda ninguna casilla de barco viva.
