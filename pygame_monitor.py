# TODO break into functions and possibly classes (organize me)

import sys
import psutil
import pygame
from pygame.locals import *


def reset_pomodoro():
    return 1500, 300, 0

def main():
    """ Script to run the system monitor

    Returns
    -------
    None
    """
    # initialize pygame thingies
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # set some constants
    BLACK = (0, 0, 0)
    BLUE = (94, 154, 249)
    DARK_TOMATO = (153, 23, 0)
    GRAY = (178, 178, 178)
    GREEN = (0, 255, 0)
    ORANGE = (252, 151, 0)
    RED = (255, 0, 0)
    TOMATO = (255, 39, 0)
    WHITE = (255, 255, 255)
    YELLOW = (232, 228, 0)
    FPS = 1
    DEFAULT_FONT = pygame.font.get_default_font()

    # create some objects
    Display = pygame.display.set_mode((320, 230))
    MyFont = pygame.font.Font(DEFAULT_FONT, 16)
    pygame.display.set_caption('System Monitor')
    Beep = pygame.mixer.Sound('beep.wav')
    Click = pygame.mixer.Sound('click.wav')
    Clock = pygame.time.Clock()

    def render_rects(percent, v_offset):
        """ renders rectangles illustrating resource usage

        Parameters
        ----------
        percent : float
            percent usage for CPU or memory
        v_offset
            vertical offset for rectangles (0 for CPU and 60 for memory)

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
            pygame.draw.rect(Display, color, (10 + i, 10 + v_offset, 12, 25), width)
            i += 15

    work_time, rest_time, over_time = reset_pomodoro()
    reset_button = pygame.Rect(190, 145, 90, 60)
    # action loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if reset_button.collidepoint(event.pos):
                        work_time, rest_time, over_time = reset_pomodoro()
                        Click.play()
        Display.fill(BLACK)
        # CPU usage
        cpu_perc = psutil.cpu_percent()
        render_rects(percent=cpu_perc, v_offset=0)
        cpu_text = MyFont.render('CPU usage:  {}%'.format(cpu_perc),
                                 True,
                                 GRAY)
        Display.blit(cpu_text, (10, 45))
        # memory usage
        mem_perc = psutil.virtual_memory()[2]
        render_rects(percent=mem_perc, v_offset=60)
        mem_text = MyFont.render('Memory usage:  {}%'.format(mem_perc),
                                 True,
                                 GRAY)
        Display.blit(mem_text, (10, 105))

        pygame.draw.rect(Display, DARK_TOMATO, (190, 145, 90, 60))
        pygame.draw.rect(Display, TOMATO, (195, 150, 80, 50))
        reset_text = MyFont.render('RESET', True, WHITE)
        Display.blit(reset_text, (207, 168))

        work_min, work_sec = divmod(work_time, 60)
        if work_sec < 10:
            work_sec = '0{}'.format(work_sec)
        work_time_text = MyFont.render('Work time:  {0}:{1}'.format(work_min, work_sec),
                                  True,
                                  GRAY)
        Display.blit(work_time_text, (10, 150))

        if work_time > 0:
            work_time -= 1

        if work_time >= 0 and rest_time > 0:
            rest_min, rest_sec = divmod(rest_time, 60)
            sign = ''
            if work_time == 0:
                rest_time -= 1
        else:
            rest_min, rest_sec = divmod(over_time, 60)
            over_time += 1
            sign = '-'
        if rest_sec < 10:
            rest_sec = '0{}'.format(rest_sec)
        rest_time_text = MyFont.render('Rest time:  {0}{1}:{2}'.format(sign, rest_min, rest_sec),
                                       True,
                                       BLUE)
        Display.blit(rest_time_text, (10, 180))

        if work_time == 0 and rest_time >= 295:
            Beep.play()

        # refresh display
        pygame.display.update()
        Clock.tick(FPS)


if __name__ == '__main__':
    main()
