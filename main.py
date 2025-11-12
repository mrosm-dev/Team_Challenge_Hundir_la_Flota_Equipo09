'''
Import necesarios
'''
import tablero
import barco
import usuario

def innit():
    '''
    Creación de tableros con barcos posicionados
    '''
    ia = usuario()
    jugador = usuario()
    
    tablero_ia = tablero() # argumentos
    tablero_jugador = tablero() # argumentos
    
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
    innit()
    update()
    end()
    pass

if __name__ == "main":
    main()