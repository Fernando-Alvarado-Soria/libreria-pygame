import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
size = (800, 600)
WIDTH, HEIGHT = size

# Crear la ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Game - Esquiva los Meteoros")

# Cargar la imagen de fondo
background_image = pygame.image.load("Recursos/fondo1.jpg")
background_image = pygame.transform.scale(background_image, size)

# Cargar sprites
nave_image = pygame.image.load("Recursos/nave/personaje.png")
meteoro_image = pygame.image.load("Recursos/meteoro/meteoro.png")



# Clase para la nave del jugador
class Nave:
    def __init__(self):
        self.image = nave_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Clase para los meteoros
class Meteoro:
    def __init__(self):
        self.image = meteoro_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Crear instancias
nave = Nave()
meteoros = []

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Contador para generar meteoros
meteoro_timer = 0

# Variables de estado del juego
game_over = False
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def reset_game():
    global nave, meteoros, meteoro_timer, game_over
    nave = Nave()
    meteoros = []
    meteoro_timer = 0
    game_over = False

# Bucle principal donde se ejecuta el juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Reiniciar juego si está en Game Over y se presiona SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reset_game()

    if not game_over:
        # Actualizar nave
        nave.update()

        # Generar meteoros
        meteoro_timer += 1
        if meteoro_timer > 60:  # Generar cada 60 frames (1 segundo a 60 FPS)
            meteoros.append(Meteoro())
            meteoro_timer = 0

        # Actualizar meteoros
        for meteoro in meteoros[:]:
            meteoro.update()
            # Eliminar meteoros que salieron de la pantalla
            if meteoro.rect.top > HEIGHT:
                meteoros.remove(meteoro)

        # Detectar colisiones
        for meteoro in meteoros[:]:
            if nave.rect.colliderect(meteoro.rect):
                game_over = True

    # Dibujar todo
    screen.blit(background_image, (0, 0))
    
    if not game_over:
        nave.draw(screen)
        for meteoro in meteoros:
            meteoro.draw(screen)
    else:
        # Dibujar nave y meteoros en posición final
        nave.draw(screen)
        for meteoro in meteoros:
            meteoro.draw(screen)
        
        # Mostrar mensaje de Game Over
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        restart_text = small_font.render("Presiona ESPACIO para reiniciar", True, (255, 255, 255))
        
        # Centrar textos
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)  # 60 FPS