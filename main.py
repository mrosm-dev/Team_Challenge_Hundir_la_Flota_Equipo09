'''
Import necesarios
'''
from tablero import Tablero
from barco import Barcos
from usuario import Usuario
import modulo_funciones as mf

def init():
    '''
    Creación de tableros con barcos posicionados
    '''
    ia = Usuario()
    jugador = Usuario()
    
    barcos_ia = Barcos()
    barcos_jugador = Barcos()
    
    tablero_ia = Tablero(barcos_ia) # argumentos
    tablero_jugador = Tablero(barcos_jugador) # argumentos
    
    tablero_ia.crear_tablero()
    pass

def update():
    '''
    Lógica de juego
        - Donde quieres disparar
        - Comprobar si hemos acertado o no
        - Comprobar si el juego ha terminado
        - Pasar siguiente jugador
    '''
    pass

def end():
    '''
    Colocar output gáfico (print) representando como han 
    quedado los tableros.
    '''
    pass

def main():
    init()
    update()
    end()
    pass

if __name__ == "main":
    main()