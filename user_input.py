import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown, DropdownChoice

import physics as phys

WHITE = (255, 255, 255)
BUTTON_COLOR = (240, 240, 240)
BLACK = (0, 0, 0)


class UserInput:
    EPS = 1e-06
    MIN_a = 0.001
    MAX_a = 0.6
    MIN_b = 5
    MAX_b = 60
    MIN_TEMP = 0.1
    MAX_TEMP = phys.MAX_TEMP
    BORDER_WIDTH = 2
    INTERNAL_LINE_WIDTH = 1

    def __init__(self, win, x, y, width, height,
                 big_font_size=30, middle_font_size=25, little_font_size=23,
                 on_click1=lambda: None,
                 on_click2=lambda: None,
                 on_click3=lambda: None):

        line_height = height // 10
        self.line_height = line_height
        apply_buttons_width = width // 4
        apply_buttons_text = "Применить"

        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.big_font_size = big_font_size
        self.middle_font_size = middle_font_size
        self.little_font_size = little_font_size
        self.on_click1 = on_click1
        self.on_click2 = on_click2
        self.on_click3 = on_click3

        self.title1 = TextBox(
            win, x, y, width * 5 // 8, line_height, fontSize=big_font_size,
            colour=WHITE, borderThickness=0
        )
        self.title1.disable()
        self.title1.setText("Конфигурация газа")

        self.apply_button1 = Button(
            win, x + width * 3 // 4, y, apply_buttons_width, line_height,
            onClick=self._on_click1_decorated,
            text=apply_buttons_text, fontSize=middle_font_size,
            inactiveColour=WHITE, pressedColour=WHITE
        )
        self.apply_button1.disable()

        self.real_gas_text = TextBox(
            win, x, y + line_height, width * 4 // 9, line_height,
            fontSize=middle_font_size, colour=WHITE, borderColour=BUTTON_COLOR
        )
        self.real_gas_text.disable()
        self.real_gas_text.setText("Реальный газ:")

        self.real_gas_dropdown = Dropdown(
            win, x + self.real_gas_text.getWidth(), self.real_gas_text.getY(),
            width // 4, line_height,
            name="*не выбран*",
            choices=list(phys.a_b_for_real_gases.keys()),
            fontSize=little_font_size, inactiveColour=BUTTON_COLOR,
        )

        self.confirmed_a = (self.MIN_a + self.MAX_a) / 2
        self.a_output = TextBox(
            win, x, y + 2 * line_height, width // 4, line_height,
            fontSize=middle_font_size, colour=WHITE, borderColour=BUTTON_COLOR,
            borderThickness=0
        )
        self.a_output.disable()

        self.a_slider = Slider(
            win,
            x + self.a_output.getWidth(),
            self.a_output.getY() + line_height // 2,
            (width - self.a_output.getWidth()) * 7 // 8, line_height // 4,
            min=self.MIN_a, max=self.MAX_a, step=0.001
        )
        self.a_slider.setValue(self.confirmed_a)

        self.confirmed_b = (self.MIN_b + self.MAX_b) / 2
        self.b_output = TextBox(
            win, x, y + 3 * line_height, width // 4, line_height,
            fontSize=middle_font_size, colour=WHITE, borderColour=BUTTON_COLOR,
            borderThickness=0
        )
        self.b_output.disable()

        self.b_slider = Slider(
            win,
            x + self.b_output.getWidth(),
            self.b_output.getY() + line_height // 2,
            (width - self.b_output.getWidth()) * 7 // 8, line_height // 4,
            min=self.MIN_b, max=self.MAX_b, step=0.5
        )
        self.b_slider.setValue(self.confirmed_b)

        self.prev_a = self.confirmed_a
        self.prev_b = self.confirmed_b

        self.title2 = TextBox(
            win, x, y + 4 * line_height, width * 5 // 8, line_height,
            fontSize=big_font_size,
            colour=WHITE, borderThickness=0
        )
        self.title2.disable()
        self.title2.setText("Изменить температуру")

        self.apply_button2 = Button(
            win, x + width * 3 // 4, self.title2.getY(),
            apply_buttons_width, line_height,
            onClick=self._on_click2_decorated,
            text=apply_buttons_text, fontSize=middle_font_size,
            inactiveColour=WHITE, pressedColour=WHITE
        )
        self.apply_button2.disable()

        self.T_text = TextBox(
            win, x, y + 5 * line_height, width // 8, line_height,
            fontSize=middle_font_size, colour=WHITE, borderColour=BUTTON_COLOR
        )
        self.T_text.disable()
        self.T_text.setText("T:")
        self.prev_T = None
        self.T_dropdown = None

        self.MIN_p = None
        self.MAX_p = None
        self.MIN_VOL = None
        self.MAX_VOL = None

        self._update_temp()

        self.title3 = TextBox(
            win, x, y + 6 * line_height, width * 5 // 8, line_height,
            fontSize=big_font_size,
            colour=WHITE, borderThickness=0
        )
        self.title3.disable()
        self.title3.setText("Изменить давление/объём")

        self.apply_button3 = Button(
            win, x + width * 3 // 4, self.title3.getY(),
            apply_buttons_width, line_height,
            onClick=self._on_click3_decorated,
            text=apply_buttons_text, fontSize=middle_font_size,
            inactiveColour=WHITE, pressedColour=WHITE
        )
        self.apply_button3.disable()

        self.p_output = TextBox(
            win, x, y + 7 * line_height, width // 4, line_height,
            fontSize=middle_font_size, colour=WHITE, borderColour=BUTTON_COLOR,
            borderThickness=0
        )
        self.p_output.disable()

        self.vol_output = TextBox(
            win, x, y + 8 * line_height, width // 4, line_height,
            fontSize=middle_font_size, colour=WHITE, borderColour=BUTTON_COLOR,
            borderThickness=0
        )
        self.vol_output.disable()

        self.p_slider = None
        self.vol_slider = None
        self.prev_p = None
        self.prev_vol = None
        self.confirmed_p = None
        self.confirmed_vol = None
        self._update_press_vol()

        self.speed_choices = ["x1", "x2", "x4", "x8"]
        self.speed_values = [1, 2, 4, 8]
        self.title4 = TextBox(
            win, x, y + 9 * line_height, width * 5 // 8, line_height,
            fontSize=big_font_size,
            colour=WHITE, borderColour=BUTTON_COLOR
        )
        self.title4.disable()
        self.title4.setText("Скорость анимации:")
        self.speed_dropdown = Dropdown(
            win, x + self.title4.getWidth(), self.title4.getY(),
            width // 4, line_height,
            name="*не выбрана*",
            choices=self.speed_choices,
            values=self.speed_values,
            fontSize=middle_font_size, inactiveColour=BUTTON_COLOR,
            direction="up"
        )
        self._set_speed_selected(0)  # x1

        self.prev_confirmed_T = None
        self.prev_confirmed_p = None
        self.prev_confirmed_vol = None

        self.apply_button1_was_disabled = True
        self.apply_button2_was_disabled = True
        self.apply_button3_was_disabled = True

        self.border_rect = pygame.Rect(x, y, width, height)

    def _update_temp(self):
        if self.T_dropdown is not None:
            self.T_dropdown.hide()

        self.temps = self._get_temps()
        self.T_dropdown = Dropdown(
            self.win, self.x + self.T_text.getWidth(), self.T_text.getY(),
            self.width // 4, self.line_height,
            name="*не выбрана*",
            choices=list(
                map(lambda elem: str(round(elem, 1)) + " K", self.temps)
            ),
            values=self.temps,
            fontSize=self.little_font_size, inactiveColour=BUTTON_COLOR,
            direction="up"
        )
        self._set_temp_selected(3)  # crit temp
        self.confirmed_T = self.T_dropdown.getSelected()
        self.prev_T = self.confirmed_T

        self.prev_p = None
        self.prev_vol = None
        self.confirmed_p = None
        self.confirmed_vol = None

        (self.MIN_TEMP_LIST_p, self.MAX_TEMP_LIST_p,
         self.MIN_VOL, self.MAX_VOL,
         self.MIN_VOL_M3, self.MAX_VOL_M3) = (
            self._calc_borders_for_press_vol_temp_list()
        )

    def _update_press_vol(self):
        if self.p_slider is not None:
            self.p_slider.hide()

        if self.vol_slider is not None:
            self.vol_slider.hide()

        self.MIN_p, self.MAX_p = phys.calc_borders_for_press(
            *self.get_confirmed_a_b_SI(),
            self.get_confirmed_temp(),
            self.MIN_VOL_M3,
            self.MAX_VOL_M3
        )

        self.MIN_p = phys.p_to_atm(self.MIN_p) + self.EPS
        self.MAX_p = phys.p_to_atm(self.MAX_p) - self.EPS
        p_slider_step = 1 if self.MIN_p > 10 else 0.01
        self.p_slider = Slider(
            self.win,
            self.x + self.p_output.getWidth() * 1.4,
            self.p_output.getY() + self.line_height // 2,
            (self.width - self.p_output.getWidth() * 1.4) * 14 // 15,
            self.line_height // 4,
            min=self.MIN_p, max=self.MAX_p, step=p_slider_step
        )

        self.vol_slider = Slider(
            self.win,
            self.x + self.vol_output.getWidth() * 1.4,
            self.vol_output.getY() + self.line_height // 2,
            (self.width - self.vol_output.getWidth() * 1.4) * 14 // 15,
            self.line_height // 4,
            min=self.MIN_VOL, max=self.MAX_VOL, step=1
        )

        if self.confirmed_p is None:
            self.confirmed_p = (self.MIN_p + self.MAX_p) / 2
            self.confirmed_vol = self._calc_vol_cm3(self.confirmed_p)
        else:
            # self.confirmed_vol = const
            self.confirmed_p = self._calc_press_atm(self.confirmed_vol)

        self.prev_p = self.confirmed_p
        self.prev_vol = self.confirmed_vol

        self.p_slider.setValue(self.confirmed_p)
        self.vol_slider.setValue(self.confirmed_vol)

    def _set_temp_selected(self, i):
        """
        Делает нужную температуру выбранной в выпадающем меню

        :param i: индекс нужной температуры в списке self.temps
        """
        temp = self.temps[i]
        default_temp_choice = DropdownChoice(
            self.win, self.T_dropdown.getX(), self.T_dropdown.getY(),
            self.T_dropdown.getWidth(), self.T_dropdown.getHeight(),
            text=str(round(temp, 1)) + " K", dropdown=self.T_dropdown,
            value=temp, last=(i == len(self.temps) - 1),
            fontSize=self.little_font_size, inactiveColour=BUTTON_COLOR,
            direction="up"
        )
        self.T_dropdown.chosen = default_temp_choice

    def _set_speed_selected(self, i):
        speed = self.speed_values[i]
        speed_str = self.speed_choices[i]
        default_speed_choice = DropdownChoice(
            self.win, self.speed_dropdown.getX(), self.speed_dropdown.getY(),
            self.speed_dropdown.getWidth(), self.speed_dropdown.getHeight(),
            text=speed_str, dropdown=self.speed_dropdown,
            value=speed, last=(i == len(self.speed_values) - 1),
            fontSize=self.middle_font_size, inactiveColour=BUTTON_COLOR,
            direction="up"
        )
        self.speed_dropdown.chosen = default_speed_choice

    def _calc_borders_for_press_vol_temp_list(self):
        a, b = self.get_confirmed_a_b_SI()

        min_p, max_p, min_vol, max_vol = \
            phys.calc_borders_for_press_vol_temp_list(
                a, b, self.temps[0], self.temps[-1]
            )

        return (phys.p_to_atm(min_p), phys.p_to_atm(max_p),
                phys.vol_to_cm3(min_vol), phys.vol_to_cm3(max_vol),
                min_vol, max_vol)

    def _calc_vol_cm3(self, p_atm):
        return phys.vol_to_cm3(phys.calc_volume(
            self.confirmed_T,
            phys.p_to_pas(p_atm),
            *self.get_confirmed_a_b_SI(),
            self.MIN_VOL_M3,
            self.MAX_VOL_M3
        ))

    def _calc_press_atm(self, vol_cm3):
        return phys.p_to_atm(phys.calc_press(
            self.confirmed_T,
            phys.vol_to_m3(vol_cm3),
            *self.get_confirmed_a_b_SI()
        ))

    def set_on_click_funcs(self,
                           on_click1=lambda: None,
                           on_click2=lambda: None,
                           on_click3=lambda: None):
        self.on_click1 = on_click1
        self.on_click2 = on_click2
        self.on_click3 = on_click3

    def _on_click1_decorated(self):
        self.confirmed_a = self.a_slider.getValue()
        self.confirmed_b = self.b_slider.getValue()
        self._update_temp()
        self._update_press_vol()
        self.apply_button1.disable()
        self.apply_button2.disable()
        self.apply_button3.disable()

        self.on_click1()

    def _on_click2_decorated(self):
        self.prev_confirmed_T = self.confirmed_T
        self.confirmed_T = self.T_dropdown.getSelected()
        self._update_press_vol()
        self.apply_button2.disable()

        self.on_click2()

    def _on_click3_decorated(self):
        self.prev_confirmed_p = self.confirmed_p
        self.prev_confirmed_vol = self.confirmed_vol
        self.confirmed_p = self.p_slider.getValue()
        self.confirmed_vol = self.vol_slider.getValue()
        self.apply_button3.disable()

        self.on_click3()

    def get_confirmed_a_b_SI(self):
        a = self.confirmed_a
        b = phys.b_to_SI(self.confirmed_b)
        return a, b

    def _get_temps(self) -> list[float]:
        """
        Возвращает список из 5 температур:
            3 подкритических, критическую, 1 надкритическую.
        """
        a, b = self.get_confirmed_a_b_SI()
        crit_temp = phys.calc_crit_temp(a, b)
        min_temp = phys.calc_min_temp(a, b)
        step = (crit_temp - min_temp) / 4
        temps = [min_temp + (i + 1) * step for i in range(5)]
        return temps

    def get_confirmed_temp(self):
        return self.confirmed_T

    def get_confirmed_temp_ind(self):
        conf_temp = self.get_confirmed_temp()
        for ind, temp in enumerate(self.temps):
            if abs(temp - conf_temp) < self.EPS:
                return ind

        raise ValueError

    def get_confirmed_press_atm(self):
        return self.confirmed_p

    def get_confirmed_vol_cm3(self):
        return self.confirmed_vol

    def get_anim_speed(self):
        return self.speed_dropdown.getSelected()

    def _real_gas_check(self):
        selected_gas = self.real_gas_dropdown.getSelected()
        if selected_gas is None:
            return
        a, b = phys.a_b_for_real_gases[selected_gas]
        if abs(a - self.prev_a) > self.EPS or abs(b - self.prev_b) > self.EPS:
            self.apply_button1.enable()
            self.apply_button1.inactiveColour = BUTTON_COLOR
        self.a_slider.setValue(a)
        self.b_slider.setValue(b)
        self.prev_a = a
        self.prev_b = b

    def _temp_check(self):
        if self.prev_T is None:
            return
        temp = self.T_dropdown.getSelected()
        if abs(temp - self.prev_T) > self.EPS:
            self.prev_T = temp
            self.apply_button2.enable()
            self.apply_button2.inactiveColour = BUTTON_COLOR

    def update(self, events, need_upd_all_widgets=True):
        if need_upd_all_widgets:
            pygame_widgets.update(events)
        a = self.a_slider.getValue()
        b = self.b_slider.getValue()
        p = self.p_slider.getValue()
        vol = self.vol_slider.getValue()

        self.a_output.setText(f"a = {a:.3f}")
        self.b_output.setText(f"b = {b}")

        if abs(p - self.prev_p) > self.EPS:
            vol = self._calc_vol_cm3(p)
            self.vol_slider.setValue(vol)
            self.apply_button3.enable()
            self.apply_button3.inactiveColour = BUTTON_COLOR

        if abs(vol - self.prev_vol) > self.EPS:
            p = self._calc_press_atm(vol)
            self.p_slider.setValue(p)
            self.apply_button3.enable()
            self.apply_button3.inactiveColour = BUTTON_COLOR

        self.prev_p = p
        self.prev_vol = vol

        if p > 10:
            self.p_output.setText(f"p = {int(p)} атм.")
        else:
            self.p_output.setText(f"p = {p:.2f} атм.")

        self.vol_output.setText(f"V = {int(vol)} см^3")

        if abs(a - self.prev_a) > self.EPS or abs(b - self.prev_b) > self.EPS:
            self.apply_button1.enable()
            self.apply_button1.inactiveColour = BUTTON_COLOR
            self.real_gas_dropdown.reset()
            self.prev_a = a
            self.prev_b = b

        self._real_gas_check()
        self._temp_check()

        pygame.draw.rect(self.win, BLACK, self.border_rect, self.BORDER_WIDTH)
        pygame.draw.line(self.win, BLACK,
                         (self.x, self.y + 4 * self.line_height),
                         (self.x + self.width, self.y + 4 * self.line_height),
                         width=self.INTERNAL_LINE_WIDTH)
        pygame.draw.line(self.win, BLACK,
                         (self.x, self.y + 6 * self.line_height),
                         (self.x + self.width, self.y + 6 * self.line_height),
                         width=self.INTERNAL_LINE_WIDTH)
        pygame.draw.line(self.win, BLACK,
                         (self.x, self.y + 9 * self.line_height),
                         (self.x + self.width, self.y + 9 * self.line_height),
                         width=self.INTERNAL_LINE_WIDTH)

    def disable(self):
        self.real_gas_dropdown.disable()
        self.a_slider.disable()
        self.b_slider.disable()
        self.T_dropdown.disable()
        self.p_slider.disable()
        self.vol_slider.disable()

        self.apply_button1_was_disabled = self.apply_button1._disabled
        self.apply_button2_was_disabled = self.apply_button2._disabled
        self.apply_button3_was_disabled = self.apply_button3._disabled

        self.apply_button1.disable()
        self.apply_button2.disable()
        self.apply_button3.disable()

    def enable(self):
        self.real_gas_dropdown.enable()
        self.a_slider.enable()
        self.b_slider.enable()
        self.T_dropdown.enable()
        self.p_slider.enable()
        self.vol_slider.enable()

        if not self.apply_button1_was_disabled:
            self.apply_button1.enable()

        if not self.apply_button2_was_disabled:
            self.apply_button2.enable()

        if not self.apply_button3_was_disabled:
            self.apply_button3.enable()


if __name__ == "__main__":
    pygame.init()
    info_obj = pygame.display.Info()
    screen_width, screen_height = info_obj.current_w, info_obj.current_h
    width, height = (screen_width // 4, screen_height // 2)

    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    user_input = UserInput(win, 0, 0, width, height)


    run = True
    while run:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill(WHITE)
        user_input.update(events)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()
        clock.tick(60)
