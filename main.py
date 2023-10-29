import pygame
import sys
from button import Button
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
from demo_screen import DemoScreen


class App:
    def __init__(self):
        pygame.init()
        info_obj = pygame.display.Info()
        self.width = info_obj.current_w
        self.height = info_obj.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.menu_screen = MenuScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.demo_screen = DemoScreen(self)

        self.active_screen = self.menu_screen

    def run(self):
        """Запуск основного цикла"""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self.active_screen._check_events()
            self.active_screen._update_screen()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
