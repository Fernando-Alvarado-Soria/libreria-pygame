import pygame
import sys
import os
import random

pygame.init()
pygame.mixer.init()  # Inicializar el mixer para audio

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

# Cargar el gato para puntos
gato_path = os.path.join("Recursos", "gatoPuntos.png")
gato_img = pygame.image.load(gato_path)
# Redimensionar para la interfaz
gato_img = pygame.transform.scale(gato_img, (30, 30))
# Versión más grande para el powerup
gato_powerup_img = pygame.transform.scale(gato_img, (50, 50))

# Cargar audio
try:
    intro_audio_path = os.path.join("Recursos", "Intro.mp3")
    pygame.mixer.music.load(intro_audio_path)
    audio_disponible = True
except pygame.error:
    print("Advertencia: No se pudo cargar el archivo de audio. El juego continuará sin música.")
    audio_disponible = False

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

# Sistema de puntuación
puntos = 0
contador_supervivencia = 0  # Para puntos por supervivencia

# Sistema de powerup de gato (puntos)
gato_en_pantalla = None
tiempo_gato_spawn = 60 * 60  # 1 minuto en frames
contador_gato_spawn = 0
valor_gato_puntos = 50  # Puntos que da el gato

# Sistema de rayo (powerup por puntos)
rayo_disponible = False  # Si el jugador puede usar el rayo
rayo_activo = False
tiempo_rayo = 15 * 60  # 15 segundos de rayo
contador_tiempo_rayo = 0
puntos_para_rayo = 100  # Cada 100 puntos se activa el rayo
ultimo_rayo_activado = 0  # Para trackear cuándo fue el último rayo
rayos = []  # Lista para almacenar los rayos activos

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

# Función para crear un powerup de gato (puntos)
def crear_gato_powerup():
    gato_rect = gato_powerup_img.get_rect()
    gato_rect.centerx = random.randint(gato_rect.width//2, size[0] - gato_rect.width//2)
    gato_rect.bottom = 0
    velocidad = 2  # Velocidad lenta para facilitar captura
    return {'rect': gato_rect, 'velocidad': velocidad}

# Función para crear un disparo
def crear_disparo(x, y):
    disparo_rect = pygame.Rect(x, y, 5, 10)  # Rectángulo pequeño para el disparo
    return {'rect': disparo_rect}

# Función para crear un rayo
def crear_rayo(x):
    rayo_rect = pygame.Rect(x, 0, 8, size[1])  # Línea vertical que cubre toda la pantalla
    return {'rect': rayo_rect, 'duracion': 10}  # El rayo dura 10 frames visible

# Función para reiniciar el juego
def reiniciar_juego():
    global meteoros, contador_meteoros, juego_activo, game_over
    global arma_en_pantalla, contador_arma_spawn, puede_disparar, contador_tiempo_disparo, disparos, vidas
    global vida_en_pantalla, contador_vida_spawn
    global puntos, contador_supervivencia, gato_en_pantalla, contador_gato_spawn
    global rayo_activo, contador_tiempo_rayo, ultimo_rayo_activado
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
    # Reiniciar sistema de puntuación
    puntos = 0
    contador_supervivencia = 0
    gato_en_pantalla = None
    contador_gato_spawn = 0
    rayo_disponible = False
    rayo_activo = False
    contador_tiempo_rayo = 0
    ultimo_rayo_activado = 0
    rayos.clear()

# Crear meteoros iniciales
for i in range(5):
    meteoros.append(crear_meteoro())

# Velocidades
velocidad_personaje = 5

# Estado del juego
juego_activo = True
game_over = False

clock = pygame.time.Clock()

# Reproducir música de fondo
if audio_disponible:
    try:
        pygame.mixer.music.play(-1)  # -1 para loop infinito
        pygame.mixer.music.set_volume(0.5)  # Volumen al 50%
    except pygame.error:
        print("Advertencia: No se pudo reproducir el audio.")

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
        
        # Detectar rayo con flecha arriba
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if not game_over and rayo_activo:  # Cambiado de rayo_disponible a rayo_activo
                # Crear rayo desde la posición del personaje
                rayo = crear_rayo(personaje_rect.centerx - 4)
                rayos.append(rayo)
                # No cambiar rayo_disponible aquí, se puede usar múltiples veces
    
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
        
        # Sistema de puntuación por supervivencia (1 punto cada segundo)
        contador_supervivencia += 1
        if contador_supervivencia >= 60:  # Cada segundo (60 frames)
            puntos += 1
            contador_supervivencia = 0
        
        # Verificar si se puede activar el rayo
        puntos_totales_para_rayo = (puntos // puntos_para_rayo) * puntos_para_rayo
        if puntos_totales_para_rayo > ultimo_rayo_activado and not rayo_activo:
            rayo_disponible = True  # Hacer disponible el rayo
            rayo_activo = True  # Activar período de 15 segundos
            contador_tiempo_rayo = tiempo_rayo
            ultimo_rayo_activado = puntos_totales_para_rayo
        
        # Manejar tiempo del rayo (período activo de 15 segundos)
        if rayo_activo:
            contador_tiempo_rayo -= 1
            if contador_tiempo_rayo <= 0:
                rayo_activo = False
                rayo_disponible = False  # Ya no se puede usar más hasta el siguiente hito
        
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
        
        # Sistema de spawn del gato (puntos) cada 1 minuto
        contador_gato_spawn += 1
        if contador_gato_spawn >= tiempo_gato_spawn and gato_en_pantalla is None:
            gato_en_pantalla = crear_gato_powerup()
            contador_gato_spawn = 0
        
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
        
        # Mover el gato (puntos) si está en pantalla
        if gato_en_pantalla is not None:
            gato_en_pantalla['rect'].y += gato_en_pantalla['velocidad']
            
            # Verificar colisión con el personaje
            if personaje_rect.colliderect(gato_en_pantalla['rect']):
                # Agregar puntos
                puntos += valor_gato_puntos
                gato_en_pantalla = None  # Eliminar gato
            
            # Eliminar gato si sale de pantalla
            elif gato_en_pantalla['rect'].top > size[1]:
                gato_en_pantalla = None
        
        # Mover disparos
        disparos_activos = []
        for disparo in disparos:
            disparo['rect'].y -= velocidad_disparo
            
            # Mantener disparos que no hayan salido de pantalla
            if disparo['rect'].bottom > 0:
                disparos_activos.append(disparo)
        
        disparos = disparos_activos
        
        # Mover rayos (reducir duración)
        rayos_activos = []
        for rayo in rayos:
            rayo['duracion'] -= 1
            if rayo['duracion'] > 0:
                rayos_activos.append(rayo)
        
        rayos = rayos_activos
        
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
                    puntos += 10  # Puntos por destruir meteoro
                    # Los disparos normales se eliminan siempre
                else:
                    disparos_restantes.append(disparo)  # Disparo no colisionó
            
            # Verificar colisión con rayos
            for rayo in rayos:
                if meteoro['rect'].colliderect(rayo['rect']):
                    meteoro_destruido = True  # Meteoro destruido por rayo
                    puntos += 15  # Más puntos por rayo (más poderoso)
                    # Los rayos no se eliminan, pueden destruir múltiples meteoros
            
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
    
    # Dibujar el gato (puntos) si está en pantalla
    if gato_en_pantalla is not None:
        screen.blit(gato_powerup_img, gato_en_pantalla['rect'])
    
    # Dibujar todos los disparos
    for disparo in disparos:
        # Disparos normales (amarillos)
        pygame.draw.rect(screen, (255, 255, 0), disparo['rect'])
    
    # Dibujar todos los rayos
    for rayo in rayos:
        # Rayo como línea vertical gruesa azul eléctrica
        pygame.draw.rect(screen, (0, 200, 255), rayo['rect'])  # Azul eléctrico
        # Efecto de brillo en los bordes
        pygame.draw.rect(screen, (255, 255, 255), rayo['rect'], 2)
        # Efecto de partículas (pequeños rectángulos alrededor)
        for i in range(5):
            offset_x = random.randint(-3, 3)
            particula_rect = pygame.Rect(rayo['rect'].x + offset_x, random.randint(0, size[1]), 2, 2)
            pygame.draw.rect(screen, (200, 230, 255), particula_rect)
    
    # Dibujar interfaz de vidas (esquina superior derecha)
    for i in range(vidas):
        x = size[0] - 40 - (i * 35)  # Posición desde la derecha
        y = 10
        screen.blit(corazon_img, (x, y))
    
    # Dibujar interfaz de puntuación (esquina superior izquierda)
    font_puntos = pygame.font.Font(None, 32)
    screen.blit(gato_img, (10, 110))  # Icono del gato
    texto_puntos = font_puntos.render(str(puntos), True, (255, 255, 255))
    screen.blit(texto_puntos, (45, 115))
    
    # Mostrar próximo rayo
    puntos_siguiente_rayo = ((puntos // puntos_para_rayo) + 1) * puntos_para_rayo
    puntos_restantes = puntos_siguiente_rayo - puntos
    font_pequena = pygame.font.Font(None, 20)
    texto_siguiente_rayo = font_pequena.render(f"Próximo rayo: {puntos_restantes} puntos", True, (200, 200, 200))
    screen.blit(texto_siguiente_rayo, (10, 145))
    
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
    
    # Mostrar estado del rayo
    if rayo_activo:
        font_pequena = pygame.font.Font(None, 24)
        texto_rayo = font_pequena.render("RAYO ACTIVO - Flecha ARRIBA", True, (0, 255, 255))
        screen.blit(texto_rayo, (10, 170))
        tiempo_rayo_restante = contador_tiempo_rayo // 60
        texto_tiempo_rayo = font_pequena.render(f"Tiempo rayo: {tiempo_rayo_restante}s", True, (0, 255, 255))
        screen.blit(texto_tiempo_rayo, (10, 195))
    
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
    
    # Mostrar si hay gato (puntos) cayendo
    if gato_en_pantalla is not None:
        font_pequena = pygame.font.Font(None, 24)
        texto_gato_cayendo = font_pequena.render(f"¡GATO CAYENDO! (+{valor_gato_puntos} pts)", True, (255, 165, 0))
        screen.blit(texto_gato_cayendo, (10, 110 if vida_en_pantalla is None else 110))
    
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