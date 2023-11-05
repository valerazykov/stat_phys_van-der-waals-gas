import pygame

pygame.init()
info_obj = pygame.display.Info()
width, height = info_obj.current_w, info_obj.current_h
old_width, old_height = (1920, 1080)


def x_rs(x_old):
    """
    Перешкалирует пиксели по оси x.
    Если раньше x изменялся на отрезке [0, 1920],
    то теперь на отрезке [0, width]
    """

    return round(x_old / old_width * width)


def y_rs(y_old):
    """
    Перешкалирует пиксели по оси y.
    Если раньше y изменялся на отрезке [0, 1080],
    то теперь на отрезке [0, height]
    """

    return round(y_old / old_height * height)
