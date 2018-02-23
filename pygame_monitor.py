import sys
import psutil
import pygame
from pygame.locals import *


def main():
    """ Script to run the system monitor

    Returns
    -------
    None
    """
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

    def render_rects(percent, v_offset):
        """ renders rectangles illustrating resource usage

        Parameters
        ----------
        percent : float
            percent usage for CPU or memory
        v_offset
            vertical offset for rectangles (0 for CPU and 85 for memory)

        Returns
        -------
        None
        """
        i = 0
        for _ in range(20):
            if 3 * percent > i :
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
            pygame.draw.rect(Display, color, (10 + i, 10 + v_offset, 12, 50), width)
            i += 15

    # action loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        Display.fill(BLACK)
        # CPU usage
        cpu_perc = psutil.cpu_percent()
        render_rects(percent=cpu_perc, v_offset=0)
        cpu_text = MyFont.render('CPU usage:  {}%'.format(cpu_perc), True, GRAY)
        Display.blit(cpu_text, (10, 70))
        # memory usage
        mem_perc = psutil.virtual_memory()[2]
        render_rects(percent=mem_perc, v_offset=85)
        mem_text = MyFont.render('Memory usage:  {}%'.format(mem_perc), True, GRAY)
        Display.blit(mem_text, (10, 155))
        # refresh display
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
