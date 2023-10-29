import pygame
import sys
from button import Button
from screen_rescale_funcs import x_rs, y_rs


class AuthorsScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35, bold=True)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50, bold=True)
        """
        self.strings = [
            "Московский Государственный Университет им. М.В. Ломоносова",
            "Факультет вычислительной математики и кибернетики",
            "Лектор: Андреев Анатолий Васильевич",
            "Руководитель: Чичигина Ольга Александровна",
            "Зыков Валерий",
            "Морозов Иван"]

        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(
                    self.middle_font.render(string, False, (0, 0, 0)))
            else:
                self.strings_surfaces.append(
                    self.little_font.render(string, False, (0, 0, 0)))

        self.text_positions = [(400, 120), (500, 170), (670, 850), (600, 790),
                               (395, 720), (1230, 720)]
        """
        self.pictures = [
            pygame.transform.scale(pygame.image.load("pictures/authors.png"),
                                   (app.width, app.height))]
        self.pictures_positions = [(0, 0)]
        self.buttons = [Button(app, "Назад", (x_rs(1500), y_rs(1000)), (x_rs(300), y_rs(80)))]

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        """
        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, self.text_positions[index])
        """

        for index, picture in enumerate(self.pictures):
            self.screen.blit(picture, self.pictures_positions[index])

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
