import pygame
import sys

pygame.init()

size = (800, 600)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mi ventana de Pygame")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()