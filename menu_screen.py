import pygame
import sys
from button import Button
from screen_rescale_funcs import x_rs, y_rs


class MenuScreen():
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35, bold=True)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50, bold=True)
        self.msu_name = "Московский Государственный Университет им. М.В. Ломоносова"
        self.faculty_name = "Факультет вычислительной математики и кибернетики"
        self.demonstration_label = "Компьютерная демонстрация по курсу"
        self.subject_name = "Статистическая физика"
        self.demonstration_name = "Процессы в газе"
        self.demonstration_name_2 = "Ван-дер-Ваальса"
        self.strings = [self.msu_name, self.faculty_name,
                        self.demonstration_label, self.subject_name,
                        self.demonstration_name, self.demonstration_name_2]
        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(
                    self.middle_font.render(string, False, (0, 0, 0)))
            elif index < 4:
                self.strings_surfaces.append(
                    self.little_font.render(string, False, (0, 0, 0)))
            else:
                self.strings_surfaces.append(
                    self.big_font.render(string, False, (0, 0, 0)))

        self.positions = [(300, 100), (450, 150), (600, 250), (720, 300),
                          (720, 400), (720, 470)]

        for i, (old_x, old_y) in enumerate(self.positions):
            self.positions[i] = (x_rs(old_x), y_rs(old_y))

        self.cmc_logo = pygame.transform.scale(
            pygame.image.load("pictures/cmc_logo.jpg"), (x_rs(140), y_rs(140)))
        self.msu_logo = pygame.transform.scale(
            pygame.image.load("pictures/msu_logo.jpg"), (x_rs(150), y_rs(150)))
        self.buttons = [Button(app, "Демонстрация", (x_rs(750), y_rs(600)),
                               (x_rs(400), y_rs(80))),
                        Button(app, "Теория", (x_rs(750), y_rs(700)),
                               (x_rs(400), y_rs(80))),
                        Button(app, "Авторы", (x_rs(750), y_rs(800)),
                               (x_rs(400), y_rs(80))),
                        Button(app, "Выход", (x_rs(750), y_rs(900)),
                               (x_rs(400), y_rs(80)))]

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, self.positions[index])
        self.screen.blit(self.cmc_logo, (x_rs(1750), y_rs(80)))
        self.screen.blit(self.msu_logo, (x_rs(50), y_rs(80)))
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
                    self.app.active_screen = self.app.demo_screen
                if index == 2:
                    self.app.active_screen = self.app.authors_screen
                elif index == 3:
                    sys.exit()
