import pygame
import sys
from time import time
import numpy as np

from button import Button
from screen_rescale_funcs import x_rs, y_rs
from user_input import UserInput
from piston import Piston
from info import Info
from pv_graph import PVGraph
import physics as phys


class DemoScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)
        self.buttons = [
            Button(app, "Назад", (x_rs(1500), y_rs(1000)), (x_rs(300), y_rs(80)))
        ]

        # -----------------
        self.EPS = 1e-8
        width, height = app.width, app.height

        self.user_input = UserInput(self.screen, 0, 0, width // 4, height // 2)
        pv_graph = PVGraph(self.screen, width // 4, 0, width * 3 // 4,
                           height * 2 // 3,
                           *self.user_input.get_confirmed_a_b_SI(),
                           self.user_input.temps,
                           (self.user_input.MIN_VOL, self.user_input.MAX_VOL))
        self.piston = Piston(
            (0, height * 0.55, width // 3, height * (1 - 0.55)),
            (self.user_input.temps[0] - self.EPS,
                self.user_input.temps[-1] + self.EPS),
            (self.user_input.MIN_VOL - self.EPS,
                self.user_input.MAX_VOL + self.EPS),
            (self.user_input.MIN_TEMP_LIST_p - self.EPS,
                self.user_input.MAX_TEMP_LIST_p + self.EPS),
            self.screen
        )
        self.info = Info(
            (width * 0.45, height * 0.55, width // 3, height * (1 - 0.55)),
            self.screen,
            round(phys.energy(
                self.user_input.get_confirmed_temp(),
                phys.vol_to_m3(self.user_input.get_confirmed_vol_cm3()),
                self.user_input.get_confirmed_a_b_SI()[0]
            ))
        )

        self.ITERATION_TIME = 4
        self.is_iteration = False
        self.time_prev_step_started = 1e12

        self.a, self.b = self.user_input.get_confirmed_a_b_SI()
        self.prev_temp = self.user_input.confirmed_T
        self.temp = self.user_input.confirmed_T
        self.prev_press = self.user_input.confirmed_p
        self.press = self.user_input.confirmed_p
        self.prev_vol = self.user_input.confirmed_vol
        self.vol = self.user_input.confirmed_vol

        self.mode_press = None
        self.mode_temp = None

        self.energy_change = 0
        self.work = 0
        self.warmth_change = 0
        # self.entropy_change = None

        self.N_STEPS = 200
        self.temp_arr = np.zeros(self.N_STEPS)
        self.vol_arr = np.zeros(self.N_STEPS)
        self.press_arr = np.zeros(self.N_STEPS)
.
        def on_click1():
            global a, b, prev_temp, temp, prev_press, press, prev_vol, vol, \
                energy_change, work, warmth_change
            a, b = user_input.get_confirmed_a_b_SI()

            prev_temp = user_input.confirmed_T
            temp = user_input.confirmed_T
            prev_press = user_input.confirmed_p
            press = user_input.confirmed_p
            prev_vol = user_input.confirmed_vol
            vol = user_input.confirmed_vol

            energy_change = 0
            work = 0
            warmth_change = 0

            pv_graph.reinit(*user_input.get_confirmed_a_b_SI(),
                            user_input.temps,
                            (user_input.MIN_VOL, user_input.MAX_VOL))
            piston.reinit(
                (0, height * 0.55, width // 3, height * (1 - 0.55)),
                (user_input.temps[0] - EPS, user_input.temps[-1] + EPS),
                (user_input.MIN_VOL - EPS, user_input.MAX_VOL + EPS),
                (user_input.MIN_TEMP_LIST_p - EPS,
                 user_input.MAX_TEMP_LIST_p + EPS),
                screen
            )

            info.reinit(
                (width * 0.45, height * 0.55, width // 3, height * (1 - 0.55)),
                screen,
                round(phys.energy(
                    user_input.get_confirmed_temp(),
                    phys.vol_to_m3(user_input.get_confirmed_vol_cm3()),
                    user_input.get_confirmed_a_b_SI()[0]
                ))
            )

        def on_click2():
            global is_iteration, time_prev_step_started, \
                a, b, prev_temp, temp, \
                prev_press, press, prev_vol, vol, mode_press, mode_temp, \
                energy_change, work, warmth_change, temp_arr, vol_arr, press_arr
            # , entropy_change

            if user_input.prev_confirmed_T is not None:
                prev_temp = user_input.prev_confirmed_T
            temp = user_input.confirmed_T

            prev_vol = user_input.confirmed_vol
            vol = user_input.confirmed_vol

            if user_input.prev_confirmed_p is not None:
                prev_press = user_input.prev_confirmed_p
            press = user_input.confirmed_p

            temps = (prev_temp, temp)
            vols = list(map(phys.vol_to_m3, (prev_vol, vol)))
            energy_change = round(phys.energy_change(temps, vols, a))
            work = round(phys.work(temps, vols, a, b))
            warmth_change = round(phys.warmth_change(temps, vols, a, b))
            # entropy_change = phys.energy_change(temps, vols, a)

            if temp > prev_temp:
                mode_temp = 1
            else:
                mode_temp = -1

            if press > prev_press:
                mode_press = 1
            else:
                mode_press = -1

            is_iteration = True

            temp_arr = np.linspace(
                np.float64(prev_temp), np.float64(temp), N_STEPS)
            vol_arr[:] = np.float64(vol)

            func = np.vectorize(
                lambda t: phys.p_to_atm(physics.calc_press(
                    t, phys.vol_to_m3(vol), a, b)
                )
            )
            press_arr = func(temp_arr)

            user_input.disable()
            time_prev_step_started = time()

        def on_click3():
            global is_iteration, time_prev_step_started, \
                a, b, prev_temp, temp, \
                prev_press, press, prev_vol, vol, mode_press, mode_temp, \
                energy_change, work, warmth_change, temp_arr, vol_arr, press_arr
            # , entropy_change

            prev_temp = user_input.confirmed_T
            temp = user_input.confirmed_T

            if user_input.prev_confirmed_vol is not None:
                prev_vol = user_input.prev_confirmed_vol
            vol = user_input.confirmed_vol

            if user_input.prev_confirmed_p is not None:
                prev_press = user_input.prev_confirmed_p
            press = user_input.confirmed_p

            temps = (prev_temp, temp)
            vols = list(map(phys.vol_to_m3, (prev_vol, vol)))
            energy_change = round(phys.energy_change(temps, vols, a))
            work = round(phys.work(temps, vols, a, b))
            warmth_change = round(phys.warmth_change(temps, vols, a, b))
            # entropy_change = phys.energy_change(temps, vols, a)

            mode_temp = 0

            if press > prev_press:
                mode_press = 1
            else:
                mode_press = -1

            is_iteration = True
            temp_arr[:] = np.float64(temp)
            vol_arr = np.linspace(
                np.float64(prev_vol), np.float64(vol), N_STEPS)

            func = np.vectorize(
                lambda v: phys.p_to_atm(
                    phys.calc_press(temp, phys.vol_to_m3(v), a, b))
            )
            press_arr = func(vol_arr)

            user_input.disable()
            time_prev_step_started = time()

        user_input.set_on_click_funcs(on_click1, on_click2, on_click3)

    def _update_screen(self):
        #self.screen.fill(self.bg_color)
        for button in self.buttons:
            button.draw_button()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)



    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen

