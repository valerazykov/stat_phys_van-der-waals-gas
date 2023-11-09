import pygame
import sys
from button import Button


class AuthorsScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.authors_picture = pygame.transform.scale(
            pygame.image.load("images/authors.png"),
            (app.width, app.height)
        )

        y_scale = 0.92
        x_scale = 0.85
        self.buttons = [
            Button(
                app, "Назад",
                (app.width * x_scale, app.height * y_scale),
                (round(app.width * (1 - x_scale)),
                 round(app.height * (1 - y_scale)))
            )
        ]

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)

        self.screen.fill(self.bg_color)
        self.screen.blit(self.authors_picture, (0, 0))

        for button in self.buttons:
            button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
