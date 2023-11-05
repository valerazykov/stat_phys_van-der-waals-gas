import sys
import pygame


def piston(screen, coor, temp, val, press, limit_temp, limit_val, limit_press,
           mode_temp, mode_press):
    """

    @param screen: объект экрана
    @param coor: кортеж (х координата левого верхнего угла,
        у координата левого верхнего угла, ширина экрана, высота экрана)
    @param temp: текущая температура
    @param val: текущий объем
    @param press: текущее давление
    @param limit_temp: кортеж из минимальной и максимальной температуры
    @param limit_val: кортеж из минимального и максимального объема
    @param limit_press: кортеж из минимального и максимального давления
    @param mode_temp: может принимать значения -1, 0, 1.
        Если -1, то изображение охлаждения, если 0, то статичная картинка,
        если 1, то изображение нагрева
    @param mode_press: может принимать значения -1, 0, 1.
        Если -1, то изображение высыпания песка,
        если 0, то статичная картинка, если 1, то изображение насыпания песка
    """
    pygame.draw.rect(screen, (255, 255, 255), coor)
    height_piston = round(0.6 * coor[3])
    width_piston = round(0.45 * coor[2])
    piston_coor = (
    coor[0] + round(0.125 * coor[2]), coor[1] + round(0.2 * coor[3]),
    width_piston, height_piston)
    pygame.draw.rect(screen, (70, 70, 70), piston_coor,
                     round(0.02 * min(coor[2], coor[3])))
    pygame.draw.rect(screen, (255, 255, 255), (
    coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
    coor[1] + round(0.2 * coor[3]),
    width_piston - 2 * round(0.02 * min(coor[2], coor[3])),
    round(0.02 * min(coor[2], coor[3]))))
    # begin_temp
    term = pygame.image.load('images/temp3.jpg')
    term = pygame.transform.scale(term,
                                  (round(0.3 * width_piston), height_piston))
    screen.blit(term, (
    coor[0] + round(0.75 * coor[2]), coor[1] + round(0.2 * coor[3])))
    temp_part = (temp - limit_temp[0]) / (limit_temp[1] - limit_temp[0])
    pygame.draw.rect(screen, (204, 1, 2), (coor[0] + round(0.8034 * coor[2]),
                                           coor[1] + round((0.28 + 0.42 * (
                                                       1 - temp_part)) * coor[
                                                               3]),
                                           round(0.0279 * coor[2]), round(
        (0.42 * temp_part + 0.03) * coor[3])))
    if mode_temp == -1:
        snow1 = pygame.image.load('images/snow1.jpg')
        snow2 = pygame.image.load('images/snow2.jpg')
        snow1 = pygame.transform.scale(snow1,
                                       (round(0.09 * coor[2]), height_piston))
        snow2 = pygame.transform.scale(snow2,
                                       (round(0.09 * coor[2]), height_piston))
        screen.blit(snow1, (
        coor[0] + round(0.0175 * coor[2]), coor[1] + round(0.2 * coor[3])))
        screen.blit(snow2, (
        coor[0] + round(0.5925 * coor[2]), coor[1] + round(0.2 * coor[3])))
    if mode_temp == 1:
        fire = pygame.image.load('images/fire.JPG')
        fire = pygame.transform.scale(fire,
                                      (width_piston, round(0.15 * coor[3])))
        screen.blit(fire, (
        coor[0] + round(0.125 * coor[2]), coor[1] + round(0.825 * coor[3])))
    myfont = pygame.font.Font('images/Roboto-Black.ttf', round(0.04 * coor[3]))
    for t in range(11):
        if t % 2 == 1:
            continue
        text_surface = myfont.render(str(round(
            limit_temp[0] + (limit_temp[1] - limit_temp[0]) * t / 10)) + ' K',
                                     True, 'Black')
        screen.blit(text_surface, (coor[0] + round(0.85 * coor[2]),
                                   coor[1] + round(
                                       (0.675 - t * 0.042) * coor[3])))
    # end_temp

    pygame.draw.rect(screen, (0, 0, 0),
                     (coor[0] + round(0.7 * coor[2]), coor[1], 2, coor[3]))
    # begin_val
    val_part = (val - limit_val[0]) / (limit_val[1] - limit_val[0])

    x = coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3]))
    gamma = 0.4 * coor[3] - 2 * round(0.02 * min(coor[2], coor[3]))
    offset = gamma - gamma * val_part
    y = coor[1] + round(0.3 * coor[3]) + round(offset)

    pygame.draw.rect(screen, (70, 70, 70), (
    x, y, width_piston - 2 * round(0.02 * min(coor[2], coor[3])),
    round(0.02 * min(coor[2], coor[3]))))
    gas = pygame.image.load('images/gas.jpg')
    gas = pygame.transform.scale(gas, (
    width_piston - 2 * round(0.02 * min(coor[2], coor[3])),
    round(coor[3] * 0.5 - 2 * round(0.02 * min(coor[2], coor[3])) - offset)))
    screen.blit(gas, (
    coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
    coor[1] + round(0.3 * coor[3]) + round(
        0.02 * min(coor[2], coor[3])) + round(offset)))
    # end_val
    # begin_press
    press_part = (press - limit_press[0]) / (limit_press[1] - limit_press[0])
    sand = pygame.image.load('images/sand.jpg')
    sand_d = pygame.image.load('images/sand_dinamic.jpg')
    sand_d = pygame.transform.scale(sand_d, (
    width_piston - 2 * round(0.02 * min(coor[2], coor[3])),
    round(0.3 * coor[3]) + round(offset)))
    if (mode_press == 1):
        screen.blit(sand_d, (
        coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
        coor[1]))
        sand = pygame.transform.scale(sand, (
            width_piston - 2 * round(0.02 * min(coor[2], coor[3])),
            round(0.1 * coor[3] * press_part)))
        screen.blit(sand, (
        coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
        coor[1] + round(0.3 * coor[3]) - round(
            0.1 * coor[3] * press_part) + round(offset)))
    # screen.blit(sand, (coor[0] + round(0.125 * coor[2]), coor[1]))
    if mode_press == 0:
        sand = pygame.transform.scale(sand, (
        width_piston - 2 * round(0.02 * min(coor[2], coor[3])),
        round(0.1 * coor[3] * press_part)))
        screen.blit(sand, (
        coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
        coor[1] + round(0.3 * coor[3]) - round(
            0.1 * coor[3] * press_part) + round(offset)))
    if mode_press == -1:
        sand_off = pygame.image.load('images/sand_off.jpg')
        sand_off = pygame.transform.scale(sand_off, (
        round(0.48125 * coor[2]), round(0.1 * coor[3] * press_part)))
        screen.blit(sand_off, (
        coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
        coor[1] + round(0.3 * coor[3]) - round(
            0.1 * coor[3] * press_part) + round(offset)))
        backet = pygame.image.load('images/backet.png')
        backet = pygame.transform.scale(backet, (
        round(0.0625 * coor[2]), round(0.0625 * coor[2])))
        screen.blit(backet, (coor[0] + round(0.575 * coor[2]),
                             coor[1] + round(0.3 * coor[3]) + round(offset)))
    # end_press
    pygame.draw.rect(screen, (70, 70, 70), (
    coor[0] + round(0.125 * coor[2]) + round(0.02 * min(coor[2], coor[3])),
    coor[1] + round(0.3 * coor[3]) - round(0.02 * min(coor[2], coor[3])),
    round(0.02 * min(coor[2], coor[3])), round(0.02 * min(coor[2], coor[3]))))
    if mode_press != -1:
        pygame.draw.rect(screen, (70, 70, 70), (
            coor[0] + round(0.125 * coor[2]) + width_piston - 2 * round(
                0.02 * min(coor[2], coor[3])),
            coor[1] + round(0.3 * coor[3]) - round(
                0.02 * min(coor[2], coor[3])),
            round(0.02 * min(coor[2], coor[3])),
            round(0.02 * min(coor[2], coor[3]))))
    pygame.display.update()


pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Our statphis")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        screen.fill((114, 157, 224))
        piston(screen, (50, 59, 700, 550), 250, 300, 200, (200, 300),
               (250, 300), (0, 300), 0, 0)
