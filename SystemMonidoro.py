import sys
import psutil
import pygame
from pygame.locals import *


class ResourceBar:

    def __init__(self, v_offset):
        """

        Parameters
        ----------
        v_offset
            vertical offset for rectangles (0 for CPU and 60 for memory)
        """
        self.v_offset = v_offset

    def render_rects(self, Display, const, percent):
        """ renders rectangles illustrating resource usage

        Parameters
        ----------
        Display : pygame display object
            display object into which the usage bar will be rendered
        const : dict
            dictionary of constants
        percent : float
            percent usage for CPU or memory

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
                color = const['GREEN']
            elif i < 180:
                color = const['YELLOW']
            elif i < 240:
                color = const['ORANGE']
            else:
                color = const['RED']
            pygame.draw.rect(Display, color, (10 + i, 10 + self.v_offset, 12, 25), width)
            i += 15


class PomodoroTimer:

    def __init__(self):
        pass

    def increment_timer(self):
        pass

    def draw_reset_button(self):
        pass

    def reset_timer(self):
        return 1500, 300, 0


class SystemMonidoro:

    def __init__(self):
        """

        """
        # initialize pygame thingies
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        # set some constants
        self.const = {
            'BLACK': (0, 0, 0),
            'BLUE': (94, 154, 249),
            'DARK_TOMATO': (153, 23, 0),
            'GRAY': (178, 178, 178),
            'GREEN': (0, 255, 0),
            'ORANGE': (252, 151, 0),
            'RED': (255, 0, 0),
            'TOMATO': (255, 39, 0),
            'WHITE': (255, 255, 255),
            'YELLOW': (232, 228, 0),
            'FPS': 1,
            'DEFAULT_FONT': pygame.font.get_default_font()
        }
        # create some objects
        self.Display = pygame.display.set_mode((320, 230))
        self.MyFont = pygame.font.Font(self.const['DEFAULT_FONT'], 16)
        pygame.display.set_caption('System Monitor')
        self.Beep = pygame.mixer.Sound('sounds/beep.wav')
        self.Click = pygame.mixer.Sound('sounds/click.wav')
        self.Clock = pygame.time.Clock()
        # instantiate some monitor bars and pomodoro timer
        self.Timer = PomodoroTimer()
        self.CPUBar = ResourceBar(v_offset=0)
        self.MemBar = ResourceBar(v_offset=60)

    def start_monitor_loop(self):
        """

        Returns
        -------

        """
        work_time, rest_time, over_time = self.Timer.reset_timer()
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
                            work_time, rest_time, over_time = self.Timer.reset_timer()
                            self.Click.play()
            self.Display.fill(self.const['BLACK'])
            # CPU usage
            cpu_perc = psutil.cpu_percent()
            render_rects(percent=cpu_perc, v_offset=0)
            cpu_text = self.MyFont.render('CPU usage:  {}%'.format(cpu_perc),
                                          True,
                                          self.const['GRAY'])
            self.Display.blit(cpu_text, (10, 45))
            # memory usage
            mem_perc = psutil.virtual_memory()[2]
            render_rects(percent=mem_perc, v_offset=60)
            mem_text = self.MyFont.render('Memory usage:  {}%'.format(mem_perc),
                                          True,
                                          self.const['GRAY'])
            self.Display.blit(mem_text, (10, 105))

            pygame.draw.rect(self.Display,
                             self.const['DARK_TOMATO'],
                             (190, 145, 90, 60))
            pygame.draw.rect(self.Display,
                             self.const['TOMATO'],
                             (195, 150, 80, 50))
            reset_text = self.MyFont.render('RESET',
                                            True,
                                            self.const['WHITE'])
            self.Display.blit(reset_text, (207, 168))

            work_min, work_sec = divmod(work_time, 60)
            if work_sec < 10:
                work_sec = '0{}'.format(work_sec)
            work_time_text = self.MyFont.render('Work time:  {0}:{1}'.format(work_min, work_sec),
                                                True,
                                                self.const['GRAY'])
            self.Display.blit(work_time_text, (10, 150))

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
            rest_time_text = self.MyFont.render('Rest time:  {0}{1}:{2}'.format(sign, rest_min, rest_sec),
                                                True,
                                                self.const['BLUE'])
            self.Display.blit(rest_time_text, (10, 180))

            if work_time == 0 and rest_time >= 295:
                self.Beep.play()

            # refresh display
            pygame.display.update()
            self.Clock.tick(self.const['FPS'])


if __name__ == '__main__':
    SM = SystemMonidoro()
    SM.start_monitor_loop()
