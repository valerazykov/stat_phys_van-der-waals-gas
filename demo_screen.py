import pygame
import pygame_widgets
from pygame_widgets.button import Button
import sys
from time import time
import numpy as np
import math

from user_input import UserInput
from piston import Piston
from info_smart import Info_smart
from pv_graph import PVGraph
import physics as phys

WHITE = (255, 255, 255)
BUTTON_COLOR = (240, 240, 240)
BUTTON_FONT_SIZE = 36
BORGER_WIDTH = 2


class DemoScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = WHITE

        self.EPS = 1e-12
        width, height = app.width, app.height

        y_scale = 0.92
        x_scale = 0.85

        def back_button_on_click():
            self.app.active_screen = self.app.menu_screen

        self.back_button = Button(self.screen,
                                  width * x_scale - BORGER_WIDTH,
                                  height * y_scale - BORGER_WIDTH,
                                  round(width * (1 - x_scale)),
                                  round(height * (1 - y_scale)),
                                  onClick=back_button_on_click,
                                  inactiveColour=BUTTON_COLOR,
                                  pressedColour=self.bg_color,
                                  text="Назад", fontSize=BUTTON_FONT_SIZE)

        self.user_input = UserInput(self.screen, BORGER_WIDTH + width // 50,
                                    height // 25,
                                    width // 4, height // 2)
        self.pv_graph = PVGraph(self.screen,
                                width // 4 + BORGER_WIDTH + width // 50,
                                0, width * 3 // 4,
                                height * 2 // 3,
                                *self.user_input.get_confirmed_a_b_SI(),
                                self.user_input.temps,
                                (self.user_input.MIN_VOL,
                                 self.user_input.MAX_VOL))
        alpha = 0.6
        bottom_margin_coef = 0.94
        self.piston = Piston(
            (BORGER_WIDTH + width // 50,
             round(height * alpha) - BORGER_WIDTH,
             width * 10 // 30,
             round(height * (1 - alpha) * bottom_margin_coef)),
            (self.user_input.temps[0] - self.EPS,
             self.user_input.temps[-1] + self.EPS),
            (self.user_input.MIN_VOL - self.EPS,
             self.user_input.MAX_VOL + self.EPS),
            (self.user_input.MIN_TEMP_LIST_p - self.EPS,
             self.user_input.MAX_TEMP_LIST_p + self.EPS),
            self.screen,
            temps=self.user_input.temps
        )
        self.info = Info_smart(
            (BORGER_WIDTH + width // 50 + width * 11 // 30,
             round(height * alpha) - BORGER_WIDTH,
             width * 0.4, round(height * (1 - alpha)) * bottom_margin_coef),
            (BORGER_WIDTH + width // 50 + width * 11 // 30 + width * 0.43,
             round(height * alpha) - BORGER_WIDTH,
             width * 0.15, height * 0.2),
            self.screen,
            round(phys.energy(
                self.user_input.get_confirmed_temp(),
                phys.vol_to_m3(self.user_input.get_confirmed_vol_cm3()),
                self.user_input.get_confirmed_a_b_SI()[0]
            )),
            self.user_input.temps[0] - self.EPS,
            self.user_input.MAX_a + self.EPS,
            self.user_input.MIN_VOL_M3 - self.EPS,
            "", "0"
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

        self.iteration_num = 0

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

            self.iteration_num = 0

            self.pv_graph.reinit(*self.user_input.get_confirmed_a_b_SI(),
                                 self.user_input.temps,
                                 (self.user_input.MIN_VOL,
                                  self.user_input.MAX_VOL))
            self.piston.reinit(
                (BORGER_WIDTH + width // 50,
                 round(height * alpha) - BORGER_WIDTH,
                 width * 10 // 30,
                 round(height * (1 - alpha) * bottom_margin_coef)),
                (self.user_input.temps[0] - self.EPS,
                 self.user_input.temps[-1] + self.EPS),
                (self.user_input.MIN_VOL - self.EPS,
                 self.user_input.MAX_VOL + self.EPS),
                (self.user_input.MIN_TEMP_LIST_p - self.EPS,
                 self.user_input.MAX_TEMP_LIST_p + self.EPS),
                self.screen,
                temps=self.user_input.temps
            )

            self.info.reinit(
                (BORGER_WIDTH + width // 50 + width * 11 // 30,
                 round(height * alpha) - BORGER_WIDTH,
                 width * 0.4,
                 round(height * (1 - alpha)) * bottom_margin_coef),
                (BORGER_WIDTH + width // 50 + width * 11 // 30 + width * 0.43,
                 round(height * alpha) - BORGER_WIDTH,
                 width * 0.15, height * 0.2),
                self.screen,
                round(phys.energy(
                    self.user_input.get_confirmed_temp(),
                    phys.vol_to_m3(self.user_input.get_confirmed_vol_cm3()),
                    self.user_input.get_confirmed_a_b_SI()[0]
                )),
                self.user_input.temps[0] - self.EPS,
                self.user_input.MAX_a + self.EPS,
                self.user_input.MIN_VOL_M3 - self.EPS,
                "", "0"
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

            self.iteration_num += 1

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
            self.info.next_iteration(self.work, self.energy_change,
                                     self.warmth_change,
                                     str(self.iteration_num - 1),
                                     str(self.iteration_num))

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

            self.iteration_num += 1

            self.mode_temp = 0

            if self.press > self.prev_press:
                self.mode_press = 1
            else:
                self.mode_press = -1

            self.is_iteration = True
            self.temp_arr[:] = np.float64(self.temp)
            self.vol_arr = np.logspace(
                np.float64(math.log(self.prev_vol)),
                np.float64(math.log(self.vol)),
                self.N_STEPS,
                base=np.e
            )

            func = np.vectorize(
                lambda v: phys.p_to_atm(
                    phys.calc_press(self.temp, phys.vol_to_m3(v),
                                    self.a, self.b))
            )
            self.press_arr = func(self.vol_arr)

            self.user_input.disable()
            self.time_prev_step_started = time()
            self.info.next_iteration(self.work, self.energy_change,
                                     self.warmth_change,
                                     str(self.iteration_num - 1),
                                     str(self.iteration_num))

        self.user_input.set_on_click_funcs(on_click1, on_click2, on_click3)
        self.iteration_step = 0

    def update_screen(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(self.bg_color)
        pygame_widgets.update(events)

        cur_temp_ind = self.user_input.get_confirmed_temp_ind()
        self.user_input.update(events, need_upd_all_widgets=False)

        if not self.is_iteration:
            if self.iteration_num == 0:
                self.pv_graph.draw(cur_temp_ind, self.vol, self.press,
                                   point_from=(self.vol, self.press),
                                   point_from_name=str(self.iteration_num))
            else:
                self.pv_graph.draw(cur_temp_ind, self.vol, self.press,
                                   point_from=(
                                   self.vol_arr[0], self.press_arr[0]),
                                   point_to=(
                                   self.vol_arr[-1], self.press_arr[-1]),
                                   point_from_name=str(self.iteration_num - 1),
                                   point_to_name=str(self.iteration_num))
            self.piston.draw(self.temp, self.vol, self.press, 0, 0)
            self.info.take_picture(self.N_STEPS - 1)
        else:
            self.pv_graph.draw(
                cur_temp_ind,
                self.vol_arr[self.iteration_step],
                self.press_arr[self.iteration_step],
                point_from=(self.vol_arr[0], self.press_arr[0]),
                point_to=(self.vol_arr[-1], self.press_arr[-1]),
                point_from_name=str(self.iteration_num - 1),
                point_to_name=str(self.iteration_num)
            )

            if self.iteration_step < self.N_STEPS - 1:
                cur_press = self.press_arr[self.iteration_step]
                next_press = self.press_arr[self.iteration_step + 1]
                if abs(cur_press - next_press) < self.EPS:
                    self.mode_press = 0
                elif cur_press < next_press:
                    self.mode_press = 1
                else:
                    self.mode_press = -1

            self.piston.draw(
                self.temp_arr[self.iteration_step],
                self.vol_arr[self.iteration_step],
                self.press_arr[self.iteration_step],
                self.mode_press,
                self.mode_temp
            )
            self.info.take_picture(self.iteration_step)

            if ((time() - self.time_prev_step_started) >
                    self.ITERATION_TIME / self.N_STEPS):
                self.time_prev_step_started = time()
                self.iteration_step += self.user_input.get_anim_speed()
                if self.iteration_step >= self.N_STEPS:
                    self.iteration_step = 0
                    self.is_iteration = False
                    self.user_input.enable()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()
