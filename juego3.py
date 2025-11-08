import pygame
import sys
import os
import random

pygame.init()

size = (800, 600)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mi ventana de Pygame")

# Cargar la imagen de fondo
fondo_path = os.path.join("Recursos", "fondo3.jpg")
fondo = pygame.image.load(fondo_path)
# Redimensionar el fondo al tamaño de la ventana
fondo = pygame.transform.scale(fondo, size)

# Cargar el personaje
personaje_path = os.path.join("Recursos", "personaje2.png")
personaje = pygame.image.load(personaje_path)
# Obtener el rectángulo del personaje para el movimiento
personaje_rect = personaje.get_rect()
# Posición inicial del personaje (centro-abajo de la pantalla)
personaje_rect.centerx = size[0] // 2
personaje_rect.bottom = size[1] - 20

# Cargar el meteoro
meteoro_path = os.path.join("Recursos", "meteoro2.png")
meteoro_img = pygame.image.load(meteoro_path)

# Cargar el arma
arma_path = os.path.join("Recursos", "arma.png")
arma_img = pygame.image.load(arma_path)

# Cargar el corazón para la interfaz de vidas
corazon_path = os.path.join("Recursos", "corazonInterfaz.png")
corazon_img = pygame.image.load(corazon_path)
# Redimensionar el corazón para la interfaz (tamaño pequeño)
corazon_img = pygame.transform.scale(corazon_img, (30, 30))

# Variables del sistema de arma
arma_en_pantalla = None  # None cuando no hay arma en pantalla
tiempo_arma_spawn = 30 * 60  # 30 segundos en frames (30 segundos * 60 FPS)
contador_arma_spawn = 0
puede_disparar = True  # Al principio puede disparar
tiempo_disparo_inicial = 7 * 60  # 7 segundos iniciales en frames
tiempo_disparo_powerup = 45 * 60  # 45 segundos con powerup en frames
contador_tiempo_disparo = tiempo_disparo_inicial  # Empezar con tiempo inicial
disparos = []  # Lista para almacenar los disparos
velocidad_disparo = 10

# Sistema de vidas
vidas = 3  # El jugador empieza con 3 vidas
vidas_maximas = 3

# Sistema de powerups de vida
vida_en_pantalla = None  # None cuando no hay powerup de vida en pantalla
tiempo_vida_spawn = 45 * 60  # 45 segundos en frames (45 segundos * 60 FPS)
contador_vida_spawn = 0
corazon_powerup_img = pygame.transform.scale(corazon_img, (40, 40))  # Versión más grande para el powerup

# Lista para almacenar múltiples meteoros
meteoros = []
# Número máximo de meteoros en pantalla
max_meteoros = 8
# Contador para crear meteoros
contador_meteoros = 0
frecuencia_meteoros = 30  # Crear un meteoro cada 30 frames (0.5 segundos a 60 FPS)

# Función para crear un nuevo meteoro
def crear_meteoro():
    meteoro_rect = meteoro_img.get_rect()
    meteoro_rect.centerx = random.randint(meteoro_rect.width//2, size[0] - meteoro_rect.width//2)
    meteoro_rect.bottom = 0
    # Velocidad aleatoria para cada meteoro (más rápida)
    velocidad = random.randint(4, 9)
    # Velocidad de rotación aleatoria (grados por frame)
    velocidad_rotacion = random.randint(-8, 8)  # Entre -8 y 8 grados por frame
    angulo = 0  # Ángulo inicial
    return {'rect': meteoro_rect, 'velocidad': velocidad, 'angulo': angulo, 'velocidad_rotacion': velocidad_rotacion}

# Función para crear el arma powerup
def crear_arma():
    arma_rect = arma_img.get_rect()
    arma_rect.centerx = random.randint(arma_rect.width//2, size[0] - arma_rect.width//2)
    arma_rect.bottom = 0
    velocidad = 3  # Velocidad más lenta para que sea más fácil agarrarla
    return {'rect': arma_rect, 'velocidad': velocidad}

# Función para crear un powerup de vida
def crear_vida_powerup():
    vida_rect = corazon_powerup_img.get_rect()
    vida_rect.centerx = random.randint(vida_rect.width//2, size[0] - vida_rect.width//2)
    vida_rect.bottom = 0
    velocidad = 2  # Velocidad aún más lenta para las vidas
    return {'rect': vida_rect, 'velocidad': velocidad}

# Función para crear un disparo
def crear_disparo(x, y):
    disparo_rect = pygame.Rect(x, y, 5, 10)  # Rectángulo pequeño para el disparo
    return {'rect': disparo_rect}

# Función para reiniciar el juego
def reiniciar_juego():
    global meteoros, contador_meteoros, juego_activo, game_over
    global arma_en_pantalla, contador_arma_spawn, puede_disparar, contador_tiempo_disparo, disparos, vidas
    global vida_en_pantalla, contador_vida_spawn
    # Reiniciar posición del personaje
    personaje_rect.centerx = size[0] // 2
    personaje_rect.bottom = size[1] - 20
    # Limpiar meteoros y crear nuevos
    meteoros.clear()
    for i in range(5):
        meteoros.append(crear_meteoro())
    # Reiniciar variables de estado
    contador_meteoros = 0
    juego_activo = True
    game_over = False
    # Reiniciar variables del arma
    arma_en_pantalla = None
    contador_arma_spawn = 0
    puede_disparar = True
    contador_tiempo_disparo = tiempo_disparo_inicial
    disparos.clear()
    # Reiniciar vidas
    vidas = vidas_maximas
    # Reiniciar variables del powerup de vida
    vida_en_pantalla = None
    contador_vida_spawn = 0

# Crear meteoros iniciales
for i in range(5):
    meteoros.append(crear_meteoro())

# Velocidades
velocidad_personaje = 5

# Estado del juego
juego_activo = True
game_over = False

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Detectar disparo con barra espaciadora
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_over and puede_disparar:
                # Crear disparo desde la posición del personaje
                disparo = crear_disparo(personaje_rect.centerx - 2, personaje_rect.top)
                disparos.append(disparo)
    
    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Si el juego terminó, solo permitir reiniciar con R
    if game_over:
        if keys[pygame.K_r]:
            reiniciar_juego()
    else:
        # Movimiento del personaje (solo si el juego está activo)
        if keys[pygame.K_LEFT] and personaje_rect.left > 0:
            personaje_rect.x -= velocidad_personaje
        if keys[pygame.K_RIGHT] and personaje_rect.right < size[0]:
            personaje_rect.x += velocidad_personaje
        
        # Sistema de tiempo de disparo
        if contador_tiempo_disparo > 0:
            contador_tiempo_disparo -= 1
        else:
            puede_disparar = False
        
        # Sistema de spawn del arma (cada 30 segundos)
        contador_arma_spawn += 1
        if contador_arma_spawn >= tiempo_arma_spawn and arma_en_pantalla is None:
            arma_en_pantalla = crear_arma()
            contador_arma_spawn = 0
        
        # Sistema de spawn del powerup de vida (cada 45 segundos)
        contador_vida_spawn += 1
        if contador_vida_spawn >= tiempo_vida_spawn and vida_en_pantalla is None:
            vida_en_pantalla = crear_vida_powerup()
            contador_vida_spawn = 0
        
        # Mover el arma si está en pantalla
        if arma_en_pantalla is not None:
            arma_en_pantalla['rect'].y += arma_en_pantalla['velocidad']
            
            # Verificar colisión con el personaje
            if personaje_rect.colliderect(arma_en_pantalla['rect']):
                # Activar poder de disparo
                puede_disparar = True
                contador_tiempo_disparo = tiempo_disparo_powerup
                arma_en_pantalla = None  # Eliminar arma
            
            # Eliminar arma si sale de pantalla
            elif arma_en_pantalla['rect'].top > size[1]:
                arma_en_pantalla = None
        
        # Mover el powerup de vida si está en pantalla
        if vida_en_pantalla is not None:
            vida_en_pantalla['rect'].y += vida_en_pantalla['velocidad']
            
            # Verificar colisión con el personaje
            if personaje_rect.colliderect(vida_en_pantalla['rect']):
                # Agregar una vida (máximo 3 vidas)
                if vidas < vidas_maximas:
                    vidas += 1
                vida_en_pantalla = None  # Eliminar powerup de vida
            
            # Eliminar powerup si sale de pantalla
            elif vida_en_pantalla['rect'].top > size[1]:
                vida_en_pantalla = None
        
        # Mover disparos
        disparos_activos = []
        for disparo in disparos:
            disparo['rect'].y -= velocidad_disparo
            
            # Mantener disparos que no hayan salido de pantalla
            if disparo['rect'].bottom > 0:
                disparos_activos.append(disparo)
        
        disparos = disparos_activos
        
        # Crear nuevos meteoros periódicamente
        contador_meteoros += 1
        if contador_meteoros >= frecuencia_meteoros and len(meteoros) < max_meteoros:
            meteoros.append(crear_meteoro())
            contador_meteoros = 0
        
        # Mover meteoros y eliminar los que salen de pantalla
        meteoros_activos = []
        for meteoro in meteoros:
            # Mover meteoro hacia abajo
            meteoro['rect'].y += meteoro['velocidad']
            
            # Rotar meteoro
            meteoro['angulo'] += meteoro['velocidad_rotacion']
            # Mantener el ángulo entre 0 y 360 grados
            meteoro['angulo'] = meteoro['angulo'] % 360
            
            # Verificar colisión con disparos
            meteoro_destruido = False
            disparos_restantes = []
            for disparo in disparos:
                if meteoro['rect'].colliderect(disparo['rect']):
                    meteoro_destruido = True  # Meteoro destruido
                else:
                    disparos_restantes.append(disparo)  # Disparo no colisionó
            
            disparos = disparos_restantes  # Actualizar lista de disparos
            
            # Solo mantener meteoro si no fue destruido
            if not meteoro_destruido:
                # Detectar colisión con el personaje
                if personaje_rect.colliderect(meteoro['rect']):
                    # Reducir una vida
                    vidas -= 1
                    # Reposicionar el personaje al centro temporalmente para evitar múltiples colisiones
                    personaje_rect.centerx = size[0] // 2
                    # Verificar si se acabaron las vidas
                    if vidas <= 0:
                        game_over = True
                        juego_activo = False
                    # No agregar este meteoro a la lista (se elimina)
                elif meteoro['rect'].top <= size[1]:
                    meteoros_activos.append(meteoro)
        
        # Actualizar la lista de meteoros
        meteoros = meteoros_activos
    
    # Dibujar el fondo
    screen.blit(fondo, (0, 0))
    
    # Dibujar el personaje
    screen.blit(personaje, personaje_rect)
    
    # Dibujar todos los meteoros
    for meteoro in meteoros:
        # Rotar la imagen del meteoro
        meteoro_rotado = pygame.transform.rotate(meteoro_img, meteoro['angulo'])
        # Obtener el nuevo rectángulo centrado en la posición original
        meteoro_rotado_rect = meteoro_rotado.get_rect(center=meteoro['rect'].center)
        # Dibujar el meteoro rotado
        screen.blit(meteoro_rotado, meteoro_rotado_rect)
    
    # Dibujar el arma si está en pantalla
    if arma_en_pantalla is not None:
        screen.blit(arma_img, arma_en_pantalla['rect'])
    
    # Dibujar el powerup de vida si está en pantalla
    if vida_en_pantalla is not None:
        screen.blit(corazon_powerup_img, vida_en_pantalla['rect'])
    
    # Dibujar todos los disparos
    for disparo in disparos:
        pygame.draw.rect(screen, (255, 255, 0), disparo['rect'])  # Disparos amarillos
    
    # Dibujar interfaz de vidas (esquina superior derecha)
    for i in range(vidas):
        x = size[0] - 40 - (i * 35)  # Posición desde la derecha
        y = 10
        screen.blit(corazon_img, (x, y))
    
    # Mostrar indicador de disparo disponible
    if puede_disparar:
        font_pequena = pygame.font.Font(None, 24)
        texto_disparo = font_pequena.render("DISPARO DISPONIBLE", True, (0, 255, 0))
        screen.blit(texto_disparo, (10, 10))
        
        # Mostrar tiempo restante
        tiempo_restante = contador_tiempo_disparo // 60  # Convertir frames a segundos
        texto_tiempo = font_pequena.render(f"Tiempo: {tiempo_restante}s", True, (0, 255, 0))
        screen.blit(texto_tiempo, (10, 35))
    else:
        font_pequena = pygame.font.Font(None, 24)
        texto_no_disparo = font_pequena.render("SIN DISPARO", True, (255, 0, 0))
        screen.blit(texto_no_disparo, (10, 10))
        
        # Mostrar tiempo hasta próxima arma
        tiempo_hasta_arma = (tiempo_arma_spawn - contador_arma_spawn) // 60
        texto_arma_tiempo = font_pequena.render(f"Próxima arma en: {tiempo_hasta_arma}s", True, (255, 255, 0))
        screen.blit(texto_arma_tiempo, (10, 35))
    
    # Mostrar si hay arma cayendo
    if arma_en_pantalla is not None:
        font_pequena = pygame.font.Font(None, 24)
        texto_arma_cayendo = font_pequena.render("¡ARMA CAYENDO!", True, (0, 255, 255))
        screen.blit(texto_arma_cayendo, (10, 60))
    
    # Mostrar si hay powerup de vida cayendo
    if vida_en_pantalla is not None:
        font_pequena = pygame.font.Font(None, 24)
        texto_vida_cayendo = font_pequena.render("¡VIDA EXTRA CAYENDO!", True, (255, 0, 255))
        screen.blit(texto_vida_cayendo, (10, 85))
    
    # Mostrar mensaje de Game Over si es necesario
    if game_over:
        # Crear fuente para el texto
        font_grande = pygame.font.Font(None, 72)
        font_pequena = pygame.font.Font(None, 36)
        
        # Crear textos
        texto_game_over = font_grande.render("GAME OVER", True, (255, 0, 0))
        texto_sin_vidas = font_pequena.render("Te quedaste sin vidas!", True, (255, 255, 255))
        texto_reiniciar = font_pequena.render("Presiona R para reiniciar", True, (255, 255, 255))
        
        # Centrar textos en la pantalla
        texto_game_over_rect = texto_game_over.get_rect(center=(size[0]//2, size[1]//2 - 60))
        texto_sin_vidas_rect = texto_sin_vidas.get_rect(center=(size[0]//2, size[1]//2 - 10))
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=(size[0]//2, size[1]//2 + 30))
        
        # Dibujar textos
        screen.blit(texto_game_over, texto_game_over_rect)
        screen.blit(texto_sin_vidas, texto_sin_vidas_rect)
        screen.blit(texto_reiniciar, texto_reiniciar_rect)
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar la velocidad de fotogramas
    clock.tick(60)