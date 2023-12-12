import pygame
import sys
from button import Button
import numpy as np
from screen_rescale_funcs import x_rs, y_rs


class TheoryScreen:
    N_IMAGES = 19
    def __init__(self, app):
        self.app = app
        self.scale = app.scale
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, int(35 * self.app.scale))
        self.middle_font = pygame.font.SysFont(self.font, int(50 * self.app.scale), bold=True)
        self.big_font = pygame.font.SysFont(self.font, int(50  * self.app.scale))
        #self.strings = ["Теория к демонстрации"]

        self.text_positions = np.array(((x_rs(700), y_rs(50)),))

        self.eng_text_positions = np.array(((x_rs(700), y_rs(50)),))

        self.theory_pictures = []


        tr_scale = 1.2

        for i in range(self.N_IMAGES):
            self.theory_pictures.append(
                pygame.transform.scale(
                    pygame.image.load(f"images/theory/{i + 1}.png"),
                    (x_rs(1478) * tr_scale, y_rs(871) * tr_scale)
                )
            )

        """
        self.theory_pictures = [pygame.transform.scale(pygame.image.load("tmp/th1.png"),
                                                (908, 596)),
                                pygame.transform.scale(pygame.image.load("tmp/th2.png"),
                                                (932, 650)),
                                pygame.transform.scale(pygame.image.load("tmp/th3.png"),
                                                (917, 570)),
                                pygame.transform.scale(pygame.image.load("tmp/th4.png"),
                                                (902, 667)),
                                pygame.transform.scale(pygame.image.load("tmp/th5.png"),
                                                (917, 556)),
                                pygame.transform.scale(pygame.image.load("tmp/th6.png"),
                                                (900, 486))]
        """

        self.active_picture = 0

        y_scale = 0.92
        x_scale = 0.9

        x_back = app.width * x_scale
        y_back = app.height * y_scale
        back_x_size = round(app.width * (1 - x_scale))
        back_y_size = round(app.height * (1 - y_scale))

        margin_right = back_x_size - x_rs(95)
        up = y_rs(20) + back_y_size

        self.buttons = [Button(app, "Назад",
                               (x_back, y_back),
                                (back_x_size, back_y_size)),
                        Button(app, "<", (x_back, y_back - up), (x_rs(90), y_rs(90))),
                        Button(app, ">", (x_back + margin_right, y_back - up), (x_rs(90), y_rs(90)))]

        self.text_pos = (x_back + x_rs(42), y_back - y_rs(170))
    
    def update_screen(self):
        self._check_events()
        self.screen.fill(self.bg_color)
        """
        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(self.middle_font.render(string, False, (0, 0, 0)))
            else:
                self.strings_surfaces.append(self.little_font.render(string, False, (0, 0, 0)))

        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, (self.text_positions[index]) * self.scale)
        """

        self.screen.blit(self.little_font.render(f"Стр. {self.active_picture + 1}/{self.N_IMAGES}",
                                                 False, (0, 0, 0)), self.text_pos)

        self.screen.blit(self.theory_pictures[self.active_picture],
                         (0, self.app.height * 0.011)
                         )

        for button in self.buttons:
            button.draw_button()

        pygame.display.flip()
    
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
                if index == 2:
                    self.active_picture = min(self.active_picture + 1, self.N_IMAGES - 1)
                if index == 1:
                    self.active_picture = max(0, self.active_picture - 1)