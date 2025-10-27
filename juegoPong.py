import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
size = (800, 600)

# Crear la ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Juego Pong")

# Reloj para controlar los FPS
clock = pygame.time.Clock()

# Fuente para mostrar el puntaje
fuente = pygame.font.Font(None, 36)

# Clase para las gotas de lluvia
class Gota:
    def __init__(self):
        self.x = random.randint(0, size[0])
        self.y = random.randint(-size[1], 0)
        self.velocidad = random.randint(2, 6)
        self.longitud = random.randint(10, 20)
    
    def caer(self):
        self.y += self.velocidad
        
        # Si la gota sale de la pantalla, reiniciarla arriba
        if self.y > size[1]:
            self.y = random.randint(-200, -10)
            self.x = random.randint(0, size[0])
            self.velocidad = random.randint(2, 6)
    
    def dibujar(self, pantalla):
        pygame.draw.line(pantalla, (173, 216, 230), (self.x, self.y), 
                        (self.x, self.y + self.longitud), 2)

# Clase para la paleta del jugador
class Paleta:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 15
        self.alto = 100
        self.velocidad = 7
    
    def mover_arriba(self):
        if self.y > 0:
            self.y -= self.velocidad
    
    def mover_abajo(self):
        if self.y < size[1] - self.alto:
            self.y += self.velocidad
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (255, 255, 255), 
                        (self.x, self.y, self.ancho, self.alto))

# Clase para la pelota
class Pelota:
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2
        self.radio = 10
        self.velocidad_x = random.choice([-5, 5])
        self.velocidad_y = random.choice([-5, 5])
    
    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
        # Rebotar en bordes superior e inferior
        if self.y - self.radio <= 0 or self.y + self.radio >= size[1]:
            self.velocidad_y *= -1
    
    def colision_paleta(self, paleta):
        # Verificar si la pelota colisiona con una paleta
        if (self.x - self.radio <= paleta.x + paleta.ancho and 
            self.x + self.radio >= paleta.x and
            self.y >= paleta.y and 
            self.y <= paleta.y + paleta.alto):
            self.velocidad_x *= -1
    
    def reiniciar(self):
        self.x = size[0] // 2
        self.y = size[1] // 2
        self.velocidad_x = random.choice([-5, 5])
        self.velocidad_y = random.choice([-5, 5])
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (255, 255, 255), (int(self.x), int(self.y)), self.radio)

# Crear lista de gotas
gotas = []
for i in range(100):  # 100 gotas de lluvia
    gotas.append(Gota())

# Crear paleta izquierda (jugador 1)
paleta_izquierda = Paleta(30, size[1] // 2 - 50)

# Crear paleta derecha (jugador 2)
paleta_derecha = Paleta(size[0] - 45, size[1] // 2 - 50)

# Crear la pelota
pelota = Pelota()

# Puntuaciones
puntos_jugador1 = 0
puntos_jugador2 = 0

# Bucle principal donde se ejecuta el juego
while True:
    # Limitar a 60 FPS
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    # Detectar teclas presionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paleta_izquierda.mover_arriba()
    if keys[pygame.K_s]:
        paleta_izquierda.mover_abajo()
    if keys[pygame.K_UP]:
        paleta_derecha.mover_arriba()
    if keys[pygame.K_DOWN]:
        paleta_derecha.mover_abajo()
    
    # Mover la pelota
    pelota.mover()
    
    # Detectar colisiones con las paletas
    pelota.colision_paleta(paleta_izquierda)
    pelota.colision_paleta(paleta_derecha)
    
    # Reiniciar si la pelota sale por los lados y actualizar puntos
    if pelota.x < 0:
        puntos_jugador2 += 1
        pelota.reiniciar()
    elif pelota.x > size[0]:
        puntos_jugador1 += 1
        pelota.reiniciar()
    
    # Fondo oscuro (cielo lluvioso)
    screen.fill((30, 30, 50))
    
    # Actualizar y dibujar las gotas
    for gota in gotas:
        gota.caer()
        gota.dibujar(screen)
    
    # Dibujar la paleta izquierda
    paleta_izquierda.dibujar(screen)
    
    # Dibujar la paleta derecha
    paleta_derecha.dibujar(screen)
    
    # Dibujar la pelota
    pelota.dibujar(screen)
    
    # Mostrar puntuaciones
    texto_jugador1 = fuente.render(str(puntos_jugador1), True, (255, 255, 255))
    texto_jugador2 = fuente.render(str(puntos_jugador2), True, (255, 255, 255))
    screen.blit(texto_jugador1, (60, 20))
    screen.blit(texto_jugador2, (size[0] - 80, 20))
    
    # Actualizar la pantalla
    pygame.display.flip()