import pygame
import sys
from button import Button
from screen_rescale_funcs import x_rs, y_rs


class DemoScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.speed = 0.5
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)
        """
        self.left_graph_position = (150, 150)
        self.right_graph_position = (1000, 150)
        self.graph_size = (650, 300)
        self.left_graph = Graph(app, [i for i in range(10)],
                                self.left_graph_position, self.graph_size,
                                True, str(1), (0, 250, 0, 10))
        self.right_graph = Graph(app, [i for i in range(10)],
                                 self.right_graph_position, self.graph_size,
                                 True, str(2), (250, 0, 0, 10))
        self.result_graph = None
        self.active_summing = False
        """
        self.buttons = [Button(app, "Назад", (x_rs(1500), y_rs(1000)), (x_rs(300), y_rs(80)))
                        # ,Button(app, "Следующий шаг", (1300, 700), (300, 80))
                        ]

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for button in self.buttons:
            button.draw_button()
        """
        if self.left_graph is not None:
            self.left_graph.draw_graph()
        if self.right_graph is not None:
            self.right_graph.draw_graph()
        if self.result_graph is not None:
            self.result_graph.draw_graph()

        if self.active_summing:
            self.summing_process()
        """

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
                self._check_graphs(mouse_position)

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
                """
                if index == 1:
                    self.start_new_lap()
                """

    def _check_graphs(self, mouse_position):
        """
        if self.left_graph.active_filling:
            self.left_graph._check_mousebutton(mouse_position)
        if self.right_graph.active_filling:
            self.right_graph._check_mousebutton(mouse_position)
        if self.result_graph is None and not self.left_graph.active_filling and not self.right_graph.active_filling:
            self.active_summing = True
        """
        pass
