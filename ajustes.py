from os import path

# Ventana
TITULO	= "Reversi"
WIDTH 	= 800
HEIGHT 	= 600
FPS 	= 30

# Colores
WHITE 	= (255,255,255)
BLACK 	= (0,0,0)
RED 	= (255,0,0)
GREEN 	= (0,255,0)
BLUE 	= (0,0,255)
YELLOW	= (255,255,0)
GREY = (155,155,155)

DIR_JUEGO 		= path.dirname(__file__)
DIR_IMAGENES 	= path.join(DIR_JUEGO,"img")
NUMEROS_TABLERO = [1,2,3,4,5,6,7,8]
