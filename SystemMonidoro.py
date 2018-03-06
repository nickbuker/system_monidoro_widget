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

    def render_rects(self, Display, CONST, percent):
        """ renders rectangles illustrating resource usage

        Parameters
        ----------
        Display : pygame display object
            display object into which the usage bar will be rendered
        CONST : dict
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
                color = CONST['GREEN']
            elif i < 180:
                color = CONST['YELLOW']
            elif i < 240:
                color = CONST['ORANGE']
            else:
                color = CONST['RED']
            pygame.draw.rect(Display, color, (10 + i, 10 + self.v_offset, 12, 25), width)
            i += 15


class PomodoroTimer:

    def __init__(self, Beep, CONST, MyFont, Display):
        """

        Parameters
        ----------
        Beep
        CONST
        MyFont
        Display
        """
        self.work_time = 1500
        self.rest_time = 300
        self.over_time = 0
        self.Beep = Beep
        self.CONST = CONST
        self.MyFont = MyFont
        self.Display = Display

    def increment_timer(self):
        """
        
        Returns
        -------

        """
        work_min, work_sec = divmod(self.work_time, 60)

        if self.work_time > 0:
            self.work_time -= 1

        if self.work_time >= 0 and self.rest_time > 0:
            rest_min, rest_sec = divmod(self.rest_time, 60)
            sign = ''
            if self.work_time == 0:
                self.rest_time -= 1

        else:
            rest_min, rest_sec = divmod(self.over_time, 60)
            self.over_time += 1
            sign = '-'

        if self.work_time == 0 and self.rest_time >= 295:
            self.Beep.play()

        return work_min, work_sec, sign, rest_min, rest_sec

    def render_time(self, work_min, work_sec, sign, rest_min, rest_sec):
        """

        Parameters
        ----------
        work_min
        work_sec
        sign
        rest_min
        rest_sec

        Returns
        -------

        """
        if work_sec < 10:
            work_sec = '0{}'.format(work_sec)
        if rest_sec < 10:
            rest_sec = '0{}'.format(rest_sec)

        work_time_text = self.MyFont.render('Work time:  {0}:{1}'.format(work_min, work_sec),
                                                                         True,
                                                                         self.CONST['GRAY'])
        self.Display.blit(work_time_text, (10, 150))

        rest_time_text = self.MyFont.render('Rest time:  {0}{1}:{2}'.format(sign, rest_min, rest_sec),
                                                                            True,
                                                                            self.CONST['BLUE'])
        self.Display.blit(rest_time_text, (10, 180))

    def draw_reset_button(self):
        """

        Returns
        -------

        """
        pygame.draw.rect(self.Display, self.CONST['DARK_TOMATO'], (190, 145, 90, 60))
        pygame.draw.rect(self.Display, self.CONST['TOMATO'], (195, 150, 80, 50))
        reset_text = self.MyFont.render('RESET', True, self.CONST['WHITE'])
        self.Display.blit(reset_text, (207, 168))

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
        self.CONST = {
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
        self.MyFont = pygame.font.Font(self.CONST['DEFAULT_FONT'], 16)
        pygame.display.set_caption('System Monitor')
        self.Beep = pygame.mixer.Sound('sounds/beep.wav')
        self.Click = pygame.mixer.Sound('sounds/click.wav')
        self.Clock = pygame.time.Clock()
        # instantiate some monitor bars and pomodoro timer
        self.Timer = PomodoroTimer(Beep=self.Beep,
                                   CONST=self.CONST,
                                   MyFont=self.MyFont,
                                   Display=self.Display)
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
            self.Display.fill(self.CONST['BLACK'])
            # CPU usage
            cpu_perc = psutil.cpu_percent()
            render_rects(percent=cpu_perc, v_offset=0)
            cpu_text = self.MyFont.render('CPU usage:  {}%'.format(cpu_perc),
                                          True,
                                          self.CONST['GRAY'])
            self.Display.blit(cpu_text, (10, 45))
            # memory usage
            mem_perc = psutil.virtual_memory()[2]
            render_rects(percent=mem_perc, v_offset=60)
            mem_text = self.MyFont.render('Memory usage:  {}%'.format(mem_perc),
                                          True,
                                          self.CONST['GRAY'])
            self.Display.blit(mem_text, (10, 105))

            pygame.draw.rect(self.Display,
                             self.CONST['DARK_TOMATO'],
                             (190, 145, 90, 60))
            pygame.draw.rect(self.Display,
                             self.CONST['TOMATO'],
                             (195, 150, 80, 50))
            reset_text = self.MyFont.render('RESET',
                                            True,
                                            self.CONST['WHITE'])
            self.Display.blit(reset_text, (207, 168))

            work_min, work_sec = divmod(work_time, 60)
            if work_sec < 10:
                work_sec = '0{}'.format(work_sec)
            work_time_text = self.MyFont.render('Work time:  {0}:{1}'.format(work_min, work_sec),
                                                True,
                                                self.CONST['GRAY'])
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
                                                self.CONST['BLUE'])
            self.Display.blit(rest_time_text, (10, 180))

            if work_time == 0 and rest_time >= 295:
                self.Beep.play()

            # refresh display
            pygame.display.update()
            self.Clock.tick(self.CONST['FPS'])


if __name__ == '__main__':
    SM = SystemMonidoro()
    SM.start_monitor_loop()
