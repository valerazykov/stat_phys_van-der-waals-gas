import pygame
import pygame_chart as pyc
import sys
import numpy as np


# pygame app for figure to run
pygame.init()
info_obj = pygame.display.Info()
width, height = info_obj.current_w, info_obj.current_h
print(width, height)
screen = pygame.display.set_mode((width, height))

# Figure instance on screen with position and size
figure1 = pyc.Figure(screen, 0, 0, width // 3, height // 3)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # add a line chart. First argument "name" should be unique for every chart
    x = np.linspace(1, 10, 100)
    figure1.line('cos', list(map(float, x)), list(map(float, np.cos(x))))
    figure1.add_xaxis_label("итерация")
    figure1.add_yaxis_label("характреистика")
    """
    figure2.line('sin', list(map(float, x)), list(map(float, np.sin(x))))
    figure3.line('log', list(map(float, x)), list(map(float, np.log(x))))
    figure4.line('exp', list(map(float, x)), list(map(float, np.exp(x))))

    figures = [figure1, figure2, figure3, figure4]
    y_labels = ["cos", "sin", "log", "exp"]

    for fig, y_label in zip(figures, y_labels):
        fig.add_xaxis_label("итерация")
        fig.add_yaxis_label(y_label)
    """

    # draw figure with specified properties
    figure1.draw()
    """
    figure2.draw()
    figure3.draw()
    figure4.draw()
    """

    pygame.display.update()