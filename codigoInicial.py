import pygame
import sys

# Inicialización de Pygame
pygame.init()

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