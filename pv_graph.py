import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import pygame

import physics
import physics as phys

mpl.use('module://pygame_matplotlib.backend_pygame')

WHITE = (255, 255, 255)


class PVGraph:
    AX_FONT_SIZE = 15
    TITLE_FONT_SIZE = 20
    X_LABEL_PAD = 10
    Y_LABEL_PAD = 0

    def _find_isotherms(
            self, a, b, temps_list, vol_limits, n_points=1000
    ):
        vol_limits = np.array(vol_limits, dtype="float64")
        self.vols = np.linspace(vol_limits[0], vol_limits[1], n_points)
        self.isotherms = np.zeros((len(temps_list), n_points))

        for i, temp in enumerate(temps_list):
            func = np.vectorize(
                lambda vol: math.log(phys.p_to_atm(
                    phys.calc_press(temp, phys.vol_to_m3(vol), a, b)))
            )
            self.isotherms[i] = func(self.vols)
            self.log_vols = np.log(self.vols)

    def __init__(
            self, win, x, y, width, height,
            a, b, temps_list, vol_limits, n_points=1000
    ):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.a = a
        self.b = b
        self.temps_list = temps_list
        self.vol_limits = vol_limits
        self._find_isotherms(
            a, b, temps_list, vol_limits, n_points
        )

    def reinit(self, a, b, temps_list, vol_limits, n_points=1000):
        self.a = a
        self.b = b
        self.temps_list = temps_list
        self.vol_limits = vol_limits
        self._find_isotherms(
            a, b, temps_list, vol_limits, n_points
        )

    def draw(self, temp_ind, vol, press):
        fig, ax = plt.subplots(
            1, 1, figsize=(self.width // 100, self.height // 100), dpi=100
        )

        for i in range(len(self.temps_list)):
            is_current = (i == temp_ind)
            color = "green" if is_current else "black"
            ax.plot(self.log_vols, self.isotherms[i], color=color)

        ax.scatter([math.log(vol)], [math.log(press)], color="red")

        ax.set_title("pV-график", fontsize=self.TITLE_FONT_SIZE)
        ax.set_xlabel("ln(V)", labelpad=self.X_LABEL_PAD,
                      fontsize=self.AX_FONT_SIZE, loc="right")
        ax.set_ylabel("ln(p)", labelpad=self.Y_LABEL_PAD,
                      fontsize=self.AX_FONT_SIZE, loc="top")
        ax.grid(True, linewidth=1)

        fig.canvas.draw()
        self.win.blit(fig, (self.x, self.y))

        plt.close()


if __name__ == "__main__":
    from user_input import UserInput
    from piston import Piston
    from info import Info
    from time import time

    EPS = 1e-8

    pygame.init()
    info_obj = pygame.display.Info()
    width, height = info_obj.current_w, info_obj.current_h

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    user_input = UserInput(screen, 0, 0, width // 4, height // 2)
    pv_graph = PVGraph(screen, width // 4, 0, width * 3 // 4, height * 2 // 3,
                       *user_input.get_confirmed_a_b_SI(),
                       user_input.temps,
                       (user_input.MIN_VOL, user_input.MAX_VOL))
    piston = Piston(
        (0, height * 0.55, width // 3, height * (1 - 0.55)),
        (user_input.temps[0] - EPS, user_input.temps[-1] + EPS),
        (user_input.MIN_VOL - EPS, user_input.MAX_VOL + EPS),
        (user_input.MIN_TEMP_LIST_p - EPS, user_input.MAX_TEMP_LIST_p + EPS),
        screen
    )
    info = Info(
        (width * 0.45, height * 0.55, width // 3, height * (1 - 0.55)),
        screen,
        round(phys.energy(
            user_input.get_confirmed_temp(),
            phys.vol_to_m3(user_input.get_confirmed_vol_cm3()),
            user_input.get_confirmed_a_b_SI()[0]
        ))
    )

    ITERATION_TIME = 4
    is_iteration = False
    time_prev_step_started = 1e12

    a, b = user_input.get_confirmed_a_b_SI()
    prev_temp = user_input.confirmed_T
    temp = user_input.confirmed_T
    prev_press = user_input.confirmed_p
    press = user_input.confirmed_p
    prev_vol = user_input.confirmed_vol
    vol = user_input.confirmed_vol

    mode_press = None
    mode_temp = None

    energy_change = 0
    work = 0
    warmth_change = 0
    # entropy_change = None

    N_STEPS = 200
    temp_arr = np.zeros(N_STEPS)
    vol_arr = np.zeros(N_STEPS)
    press_arr = np.zeros(N_STEPS)


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

    run = True
    iteration_step = 0
    while run:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        cur_temp_ind = user_input.get_confirmed_temp_ind()
        user_input.update(events)

        if not is_iteration:
            screen.fill(WHITE)
            user_input.update(events)
            pv_graph.draw(cur_temp_ind, vol, press)
            piston.draw(temp, vol, press, 0, 0)
            info.draw(work, energy_change, warmth_change,
                      199, last_draw_for_199=False)

            # Отображение последнего прорисованного экрана.
            pygame.display.flip()
        else:
            it_time = ITERATION_TIME / user_input.get_anim_speed()
            if (time() - time_prev_step_started) > it_time / N_STEPS:
                time_prev_step_started = time()

                screen.fill(WHITE)
                user_input.update(events)
                pv_graph.draw(
                    cur_temp_ind,
                    vol_arr[iteration_step], press_arr[iteration_step]
                )
                piston.draw(
                    temp_arr[iteration_step],
                    vol_arr[iteration_step],
                    press_arr[iteration_step],
                    mode_press,
                    mode_temp
                )
                info.draw(work, energy_change, warmth_change, iteration_step)
                # Отображение последнего прорисованного экрана.
                pygame.display.flip()
                iteration_step += 1
                if iteration_step == N_STEPS:
                    iteration_step = 0
                    is_iteration = False
                    user_input.enable()

    clock.tick(60)
