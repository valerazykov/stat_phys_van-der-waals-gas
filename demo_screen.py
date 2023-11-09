import pygame
import pygame_widgets
from pygame_widgets.button import Button
import sys
from time import time
import numpy as np

from user_input import UserInput
from piston import Piston
from info import Info
from pv_graph import PVGraph
import physics as phys


BUTTON_COLOR = (240, 240, 240)
BUTTON_FONT_SIZE = 36


class DemoScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)

        self.EPS = 1e-8
        width, height = app.width, app.height

        y_scale = 0.92
        x_scale = 0.85

        def back_button_on_click():
            self.app.active_screen = self.app.menu_screen

        self.back_button = Button(self.screen,
                                  width * x_scale, height * y_scale,
                                  width * (1 - x_scale),
                                  height * (1 - y_scale),
                                  onClick=back_button_on_click,
                                  inactiveColour=BUTTON_COLOR,
                                  pressedColour=self.bg_color,
                                  text="Назад", fontSize=BUTTON_FONT_SIZE)

        self.user_input = UserInput(self.screen, 0, 0, width // 4, height // 2)
        self.pv_graph = PVGraph(self.screen, width // 4, 0, width * 3 // 4,
                                height * 2 // 3,
                                *self.user_input.get_confirmed_a_b_SI(),
                                self.user_input.temps,
                                (self.user_input.MIN_VOL,
                                 self.user_input.MAX_VOL))
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

        self.saved_energy_change = 0
        self.saved_work = 0
        self.saved_warmth_change = 0

        self.N_STEPS = 200
        self.temp_arr = np.zeros(self.N_STEPS)
        self.vol_arr = np.zeros(self.N_STEPS)
        self.press_arr = np.zeros(self.N_STEPS)

        def on_click1():
            self.a, self.b = self.user_input.get_confirmed_a_b_SI()

            self.prev_temp = self.user_input.confirmed_T
            self.temp = self.user_input.confirmed_T
            self.prev_press = self.user_input.confirmed_p
            self.press = self.user_input.confirmed_p
            self.prev_vol = self.user_input.confirmed_vol
            self.vol = self.user_input.confirmed_vol

            self.energy_change = 0
            self.work = 0
            self.warmth_change = 0

            self.pv_graph.reinit(*self.user_input.get_confirmed_a_b_SI(),
                                 self.user_input.temps,
                                 (self.user_input.MIN_VOL,
                                  self.user_input.MAX_VOL))
            self.piston.reinit(
                (0, height * 0.55, width // 3, height * (1 - 0.55)),
                (self.user_input.temps[0] - self.EPS,
                 self.user_input.temps[-1] + self.EPS),
                (self.user_input.MIN_VOL - self.EPS,
                 self.user_input.MAX_VOL + self.EPS),
                (self.user_input.MIN_TEMP_LIST_p - self.EPS,
                 self.user_input.MAX_TEMP_LIST_p + self.EPS),
                self.screen
            )

            self.info.reinit(
                (width * 0.45, height * 0.55, width // 3, height * (1 - 0.55)),
                self.screen,
                round(phys.energy(
                    self.user_input.get_confirmed_temp(),
                    phys.vol_to_m3(self.user_input.get_confirmed_vol_cm3()),
                    self.user_input.get_confirmed_a_b_SI()[0]
                ))
            )

        def on_click2():
            if self.user_input.prev_confirmed_T is not None:
                self.prev_temp = self.user_input.prev_confirmed_T
            self.temp = self.user_input.confirmed_T

            self.prev_vol = self.user_input.confirmed_vol
            self.vol = self.user_input.confirmed_vol

            if self.user_input.prev_confirmed_p is not None:
                self.prev_press = self.user_input.prev_confirmed_p
            self.press = self.user_input.confirmed_p

            temps = (self.prev_temp, self.temp)
            vols = list(map(phys.vol_to_m3, (self.prev_vol, self.vol)))

            self.saved_energy_change = self.energy_change
            self.saved_work = self.work
            self.saved_warmth_change = self.warmth_change

            self.energy_change = round(phys.energy_change(temps, vols, self.a))
            self.work = round(phys.work(temps, vols, self.a, self.b))
            self.warmth_change = round(phys.warmth_change(temps, vols,
                                                          self.a, self.b))
            # self.entropy_change = phys.energy_change(temps, vols, self.a)

            if self.temp > self.prev_temp:
                self.mode_temp = 1
            else:
                self.mode_temp = -1

            if self.press > self.prev_press:
                self.mode_press = 1
            else:
                self.mode_press = -1

            self.is_iteration = True

            self.temp_arr = np.linspace(
                np.float64(self.prev_temp), np.float64(self.temp),
                self.N_STEPS)
            self.vol_arr[:] = np.float64(self.vol)

            func = np.vectorize(
                lambda t: phys.p_to_atm(phys.calc_press(
                    t, phys.vol_to_m3(self.vol), self.a, self.b)
                )
            )
            self.press_arr = func(self.temp_arr)

            self.user_input.disable()
            self.time_prev_step_started = time()

        def on_click3():
            self.prev_temp = self.user_input.confirmed_T
            self.temp = self.user_input.confirmed_T

            if self.user_input.prev_confirmed_vol is not None:
                self.prev_vol = self.user_input.prev_confirmed_vol
            self.vol = self.user_input.confirmed_vol

            if self.user_input.prev_confirmed_p is not None:
                self.prev_press = self.user_input.prev_confirmed_p
            self.press = self.user_input.confirmed_p

            temps = (self.prev_temp, self.temp)
            vols = list(map(phys.vol_to_m3, (self.prev_vol, self.vol)))

            self.saved_energy_change = self.energy_change
            self.saved_work = self.work
            self.saved_warmth_change = self.warmth_change

            self.energy_change = round(phys.energy_change(temps, vols, self.a))
            self.work = round(phys.work(temps, vols, self.a, self.b))
            self.warmth_change = round(phys.warmth_change(temps, vols, self.a,
                                                          self.b))
            # self.entropy_change = phys.energy_change(temps, vols, self.a)

            self.mode_temp = 0

            if self.press > self.prev_press:
                self.mode_press = 1
            else:
                self.mode_press = -1

            self.is_iteration = True
            self.temp_arr[:] = np.float64(self.temp)
            self.vol_arr = np.linspace(
                np.float64(self.prev_vol), np.float64(self.vol), self.N_STEPS)

            func = np.vectorize(
                lambda v: phys.p_to_atm(
                    phys.calc_press(self.temp, phys.vol_to_m3(v),
                                    self.a, self.b))
            )
            self.press_arr = func(self.vol_arr)

            self.user_input.disable()
            self.time_prev_step_started = time()

        self.user_input.set_on_click_funcs(on_click1, on_click2, on_click3)
        self.iteration_step = 0

    def _update_screen(self):
        return

    def _check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        pygame_widgets.update(events)

        cur_temp_ind = self.user_input.get_confirmed_temp_ind()
        self.user_input.update(events, need_upd_all_widgets=False)

        if not self.is_iteration:
            self.screen.fill(self.bg_color)
            self.user_input.update(events)
            self.pv_graph.draw(cur_temp_ind, self.vol, self.press)
            self.piston.draw(self.temp, self.vol, self.press, 0, 0)
            self.info.draw(self.work, self.energy_change, self.warmth_change,
                           199, last_draw_for_199=False)

            # Отображение последнего прорисованного экрана.
            # pygame.display.flip()
        else:
            if self.iteration_step == 0:
                self.info.draw(self.saved_work, self.saved_energy_change,
                               self.saved_warmth_change,
                               199, last_draw_for_199=True)
            it_time = self.ITERATION_TIME / self.user_input.get_anim_speed()
            if (time() - self.time_prev_step_started) > it_time / self.N_STEPS:
                self.time_prev_step_started = time()

                self.screen.fill(self.bg_color)
                self.user_input.update(events)
                self.pv_graph.draw(
                    cur_temp_ind,
                    self.vol_arr[self.iteration_step],
                    self.press_arr[self.iteration_step]
                )
                self.piston.draw(
                    self.temp_arr[self.iteration_step],
                    self.vol_arr[self.iteration_step],
                    self.press_arr[self.iteration_step],
                    self.mode_press,
                    self.mode_temp
                )

                self.info.draw(self.work, self.energy_change,
                               self.warmth_change, self.iteration_step, False)

                # Отображение последнего прорисованного экрана.
                # pygame.display.flip()
                self.iteration_step += 1
                if self.iteration_step == self.N_STEPS:
                    self.iteration_step = 0
                    self.is_iteration = False
                    self.user_input.enable()
