import pygame
import sys

# Inicialización de Pygame
pygame.init()

#Definir colores en RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Configuración de la ventana
size = (800, 600)

# Crear la ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mi ventana de Pygame")

# Bucle principal donde se ejecuta el juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Color de fondo
    screen.fill(WHITE)
    ### ---ZONA DE DIBUJO--- ###


    ### ---ZONA DE DIBUJO--- ###

    # actualizar la pantalla
    pygame.display.flip()
