import pygame
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
from demo_screen import DemoScreen
from theory_screen import TheoryScreen


class App:
    def __init__(self, fps=60):
        self.fps = fps
        pygame.init()
        info_obj = pygame.display.Info()
        self.width = info_obj.current_w
        self.height = info_obj.current_h
        self.scale = self.width / 1920
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.menu_screen = MenuScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.demo_screen = DemoScreen(self)
        self.theory_screen = TheoryScreen(self)

        self.active_screen = self.menu_screen

    def run(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption("Van der Waals gas")
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)
        # Запуск основного цикла
        while True:
            self.active_screen.update_screen()
            clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.run()
