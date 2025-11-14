class Tablero:
    def __init__(self, columnas, filas, usuario):
        self.usurio = usuario
        self.columnas = columnas
        self.filas = filas
        pass
    
    def crear_tablero(lado = 10, agua = "-"):
        tablero = np.full((lado,lado),agua)
        return tablero
        pass
    
    