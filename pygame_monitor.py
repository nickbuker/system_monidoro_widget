import sys
import psutil
import pygame
from pygame.locals import *

# initialize pygame thingies
pygame.init()
pygame.font.init()

# set some constants
GRAY = (178, 178, 178)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (232, 228, 0)
ORANGE = (252, 151, 0)
RED = (255, 0, 0)
FPS = 1
DEFAULT_FONT = pygame.font.get_default_font()

# create some objects
Display = pygame.display.set_mode((320, 180))
MyFont = pygame.font.Font(DEFAULT_FONT, 16)
pygame.display.set_caption('System Monitor')
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    Display.fill(BLACK)

    cpu_perc = psutil.cpu_percent()
    i = 0
    for _ in range(20):
        if 3 * cpu_perc > i :
            width = 0
        else:
            width = 1
        if i < 120:
            color = GREEN
        elif i < 180:
            color = YELLOW
        elif i < 240:
            color = ORANGE
        else:
            color = RED
        pygame.draw.rect(Display, color, (10 + i, 10, 12, 50), width)
        i += 15
    cpu_text = MyFont.render('CPU usage:  {}%'.format(cpu_perc), True, GRAY)
    Display.blit(cpu_text, (10, 70))

    mem_perc = psutil.virtual_memory()[2]
    i = 0
    for _ in range(20):
        if 3 * mem_perc > i:
            width = 0
        else:
            width = 1
        if i < 120:
            color = GREEN
        elif i < 180:
            color = YELLOW
        elif i < 240:
            color = ORANGE
        else:
            color = RED
        pygame.draw.rect(Display, color, (10 + i, 95, 12, 50), width)
        i += 15
    mem_text = MyFont.render('Memory usage:  {}%'.format(mem_perc), True, GRAY)
    Display.blit(mem_text, (10, 155))

    pygame.display.update()
    clock.tick(FPS)