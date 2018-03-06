import sys
import psutil
import pygame
from pygame.locals import *


class Resource:

    def __init__(self, cpu):
        """

        Parameters
        ----------
        cpu : bool
            True = class is for CPU resources
            False = class is for memory resourse
        """
        self.cpu = cpu

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
        if self.cpu:
            v_offset = 0
        else:
            v_offset = 60
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
            pygame.draw.rect(Display, color, (10 + i, 10 + v_offset, 12, 25), width)
            i += 15
        return

    def render_resource_text(self, MyFont, perc, CONST, Display):
        """

        Parameters
        ----------
        MyFont
        perc
        CONST
        Display

        Returns
        -------

        """
        if self.cpu:
            usage_text = 'CPU usage:  {}%'
            v_offset = 45
        else:
            usage_text = 'Memory usage:  {}%'
            v_offset = 105
        render_text = MyFont.render(usage_text.format(perc),
                                    True,
                                    CONST['GRAY'])
        Display.blit(render_text, (10, v_offset))
        return


class PomodoroTimer:

    def __init__(self):
        """

        """
        self.work_time = 1500
        self.rest_time = 300
        self.over_time = 0

    def increment_timer(self, Beep):
        """

        Parameters
        ----------
        Beep

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
            Beep.play()

        return work_min, work_sec, sign, rest_min, rest_sec

    def render_time_text(self, times, MyFont, CONST, Display):
        """

        Parameters
        ----------
        times : tuple
            (work_min, work_sec, sign, rest_min, rest_sec)
        MyFont
        CONST
        Display

        Returns
        -------

        """
        work_min, work_sec = times[0], times[1]
        sign = times[2]
        rest_min, rest_sec = times[3], times[4]
        if work_sec < 10:
            work_sec = '0{}'.format(work_sec)
        if rest_sec < 10:
            rest_sec = '0{}'.format(rest_sec)

        work_time_text = MyFont.render('Work time:  {0}:{1}'.format(work_min, work_sec),
                                                                    True,
                                                                    CONST['GRAY'])
        Display.blit(work_time_text, (10, 150))

        rest_time_text = MyFont.render('Rest time:  {0}{1}:{2}'.format(sign, rest_min, rest_sec),
                                                                       True,
                                                                       CONST['BLUE'])
        Display.blit(rest_time_text, (10, 180))
        return

    def draw_reset_button(self, Display, CONST, MyFont):
        """

        Parameters
        ----------
        Display
        CONST
        MyFont

        Returns
        -------

        """
        pygame.draw.rect(Display,
                         CONST['DARK_TOMATO'],
                         (190, 145, 90, 60))
        pygame.draw.rect(Display,
                         CONST['TOMATO'],
                         (195, 150, 80, 50))
        reset_text = MyFont.render('RESET',
                                   True,
                                   CONST['WHITE'])
        Display.blit(reset_text, (207, 168))
        return

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
        # instantiate pomodoro timer and resource monitors
        self.Timer = PomodoroTimer()
        self.CPUResource = Resource(cpu=True)
        self.MemResource = Resource(cpu=False)

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

            # memory usage
            mem_perc = psutil.virtual_memory()[2]
            render_rects(percent=mem_perc, v_offset=60)


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
