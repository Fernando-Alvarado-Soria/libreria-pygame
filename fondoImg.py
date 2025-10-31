import pygame
import sys


# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
size = (800, 600)

# Crear la ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mi ventana de Pygame")

# Cargar la imagen de fondo
# Asume que la imagen está en Recursos/fondo1/ y se llama algo como "fondo.png" o "fondo.jpg"
background_image = pygame.image.load("Recursos/fondo1.jpg")
# Escalar la imagen al tamaño de la ventana
background_image = pygame.transform.scale(background_image, size)

# Bucle principal donde se ejecuta el juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    # Dibujar la imagen de fondo
    screen.blit(background_image, (0, 0))
    
    # Actualizar la pantalla
    pygame.display.flip()