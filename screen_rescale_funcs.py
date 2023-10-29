import pygame

pygame.init()
info_obj = pygame.display.Info()
width, height = info_obj.current_w, info_obj.current_h
old_width, old_height = (1920, 1080)


def x_rs(x_old):
    return round(x_old / old_width * width)


def y_rs(y_old):
    return round(y_old / old_height * height)
