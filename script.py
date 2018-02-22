import sys
import psutil
import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

FPS = 1

DISPLAY = pygame.display.set_mode((320, 220))
pygame.display.set_caption('System Monitor')
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAY.fill(BLACK)
    cpu_perc = psutil.cpu_percent()
    print(cpu_perc)
    pygame.draw.rect(DISPLAY, BLUE, (10, 10, 3 * cpu_perc, 110))
    pygame.display.update()
    clock.tick(FPS)