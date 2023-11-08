import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import pygame

import physics as phys

mpl.use('module://pygame_matplotlib.backend_pygame')

WHITE = (255, 255, 255)


class PVGraph:
    AX_FONT_SIZE = 15
    TITLE_FONT_SIZE = 20
    X_LABEL_PAD = 10
    Y_LABEL_PAD = 35

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
            ax.plot(self.vols, self.isotherms[i], color=color)

        ax.scatter([vol], [math.log(press)], color="red")

        ax.set_title("pV-график", fontsize=self.TITLE_FONT_SIZE)
        ax.set_xlabel("V (см^3)", labelpad=self.X_LABEL_PAD,
                      fontsize=self.AX_FONT_SIZE)
        ax.set_ylabel("ln(p)", labelpad=self.Y_LABEL_PAD,
                      fontsize=self.AX_FONT_SIZE)

        fig.canvas.draw()
        self.win.blit(fig, (self.x, self.y))

        plt.close()


if __name__ == "__main__":
    from user_input import UserInput
    from piston import Piston
    from info import Info

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
        (user_input.temps[0], user_input.temps[-1]),
        (user_input.MIN_VOL, user_input.MAX_VOL),
        (user_input.MIN_TEMP_LIST_p, user_input.MAX_TEMP_LIST_p),
        screen
    )
    info = Info(
        (width * 2 // 3, height * 0.55, width // 3, height * (1 - 0.55)),
        screen,
        phys.energy(
            user_input.get_confirmed_temp(),
            phys.vol_to_m3(user_input.get_confirmed_vol_cm3()),
            user_input.get_confirmed_a_b_SI()[0]
        )
    )


    def on_click1():
        pv_graph.reinit(*user_input.get_confirmed_a_b_SI(),
                        user_input.temps,
                        (user_input.MIN_VOL, user_input.MAX_VOL))
        piston.reinit(
            (0, height * 0.55, width // 3, height * (1 - 0.55)),
            (user_input.temps[0], user_input.temps[-1]),
            (user_input.MIN_VOL, user_input.MAX_VOL),
            (user_input.MIN_TEMP_LIST_p, user_input.MAX_TEMP_LIST_p),
            screen
        )
        info.reinit(
            (width * 2 // 3, height * 0.55, width // 3, height * (1 - 0.55)),
            screen,
            phys.energy(
                user_input.get_confirmed_temp(),
                phys.vol_to_m3(user_input.get_confirmed_vol_cm3()),
                user_input.get_confirmed_a_b_SI()[0]
            )
        )

    def on_click2():
        a, b = user_input.get_confirmed_a_b_SI()
        prev_temp = user_input.prev_confirmed_T
        temp = user_input.confirmed_T
        vol = user_input.confirmed_vol
        temps = (prev_temp, temp)
        vols = (vol, vol)
        energy_change = phys.energy_change(temps, vols, a)
        work = phys.work(temps, vols, a, b)
        warmth_change = phys.warmth_change(temps, vols, a, b)
        # entropy_change = phys.energy_change(temps, vols, a)





    user_input.set_on_click_funcs(on_click1=on_click1)

    run = True
    while run:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        screen.fill(WHITE)
        user_input.update(events)

        temp = user_input.get_confirmed_temp()
        temp_ind = user_input.get_confirmed_temp_ind()
        vol = user_input.get_confirmed_vol_cm3()
        press = user_input.get_confirmed_press_atm()

        pv_graph.draw(temp_ind, vol, press)
        piston.draw(temp, vol, press, 0, 0)
        info.draw(0, 0, 0, 199, last_draw_for_199=False)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()
        clock.tick(60)
