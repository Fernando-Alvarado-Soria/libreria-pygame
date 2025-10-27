import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
size = (800, 600)

# Crear la ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Animación - Círculo en movimiento con nieve")

# Reloj para controlar los FPS
clock = pygame.time.Clock()

# Propiedades del círculo
circulo_x = 400
circulo_y = 300
circulo_radio = 30
circulo_color = (255, 100, 100)  # Rojo

# Velocidad del círculo
velocidad_x = 5
velocidad_y = 3

# Crear copos de nieve
class Copo:
    def __init__(self):
        self.x = random.randint(0, size[0])
        self.y = random.randint(-50, size[1])
        self.velocidad = random.uniform(1, 3)
        self.tamano = random.randint(2, 5)
    
    def caer(self):
        self.y += self.velocidad
        # Si el copo sale de la pantalla, vuelve a aparecer arriba
        if self.y > size[1]:
            self.y = random.randint(-20, -5)
            self.x = random.randint(0, size[0])
    
    def dibujar(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.tamano)

# Crear una lista de copos de nieve
copos = [Copo() for _ in range(100)]

# Bucle principal donde se ejecuta el juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    # Actualizar posición del círculo
    circulo_x += velocidad_x
    circulo_y += velocidad_y
    
    # Detectar colisión con los bordes y rebotar
    if circulo_x - circulo_radio <= 0 or circulo_x + circulo_radio >= size[0]:
        velocidad_x = -velocidad_x
    if circulo_y - circulo_radio <= 0 or circulo_y + circulo_radio >= size[1]:
        velocidad_y = -velocidad_y
    
    # Actualizar posición de los copos de nieve
    for copo in copos:
        copo.caer()
    
    # Limpiar la pantalla (fondo azul oscuro para simular noche)
    screen.fill((20, 24, 82))
    
    # Dibujar los copos de nieve
    for copo in copos:
        copo.dibujar(screen)
    
    # Dibujar el círculo (encima de la nieve)
    pygame.draw.circle(screen, circulo_color, (int(circulo_x), int(circulo_y)), circulo_radio)
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar los FPS (60 frames por segundo)
    clock.tick(60)