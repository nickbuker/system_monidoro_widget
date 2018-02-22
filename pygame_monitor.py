import sys
import psutil
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

GRAY = (178, 178, 178)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (232, 228, 0)
ORANGE = (252, 151, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 1

DISPLAY = pygame.display.set_mode((320, 180))
DEFAULT_FONT = pygame.font.get_default_font()
MY_FONT = pygame.font.Font(DEFAULT_FONT, 16)
pygame.display.set_caption('System Monitor')
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAY.fill(BLACK)

    cpu_perc = psutil.cpu_percent()
    pygame.draw.rect(DISPLAY, GREEN, (10, 10, 3 * cpu_perc, 50))
    cpu_text = MY_FONT.render('CPU usage:  {}%'.format(cpu_perc), True, GRAY)
    DISPLAY.blit(cpu_text, (10, 70))

    mem_perc = psutil.virtual_memory()[2]
    pygame.draw.rect(DISPLAY, ORANGE, (10, 95, 3 * mem_perc, 50))
    mem_text = MY_FONT.render('Memory usage:  {}%'.format(mem_perc), True, GRAY)
    DISPLAY.blit(mem_text, (10, 155))

    pygame.display.update()
    clock.tick(FPS)