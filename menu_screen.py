import pygame
import sys

from button import Button
from screen_rescale_funcs import x_rs, y_rs

WHITE = (255, 255, 255)
BUTTON_COLOR = (240, 240, 240)


class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = WHITE
        self.menu_picture = pygame.transform.scale(
            pygame.image.load("images/menu.png"),
            (app.width, app.height)
        )

        self.buttons = [Button(app, "Демонстрация", (x_rs(750), y_rs(600)),
                               (x_rs(400), y_rs(80))),
                        Button(app, "Теория", (x_rs(750), y_rs(700)),
                               (x_rs(400), y_rs(80))),
                        Button(app, "Авторы", (x_rs(750), y_rs(800)),
                               (x_rs(400), y_rs(80))),
                        Button(app, "Выход", (x_rs(750), y_rs(900)),
                               (x_rs(400), y_rs(80)))]

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)

        self.screen.fill(self.bg_color)
        self.screen.blit(self.menu_picture, (0, 0))
        for button in self.buttons:
            button.draw_button()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.demo_screen
                if index == 1:
                    self.app.active_screen = self.app.theory_screen
                if index == 2:
                    self.app.active_screen = self.app.authors_screen
                elif index == 3:
                    sys.exit()
