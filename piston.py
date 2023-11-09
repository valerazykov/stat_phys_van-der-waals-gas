import pygame


class Piston:
    def __init__(self, coor, limit_temp, limit_val, limit_press, screen):
        """
        :param coor: кортеж (х координата левого верхнего угла,
            у координата левого верхнего угла, ширина экрана, высота экрана)
        :param limit_temp: кортеж из минимальной и максимальной температуры
        :param limit_val: кортеж из минимального и максимального объема
        :param limit_press: кортеж из минимального и максимального давления
        :param screen: объект экрана
        """
        self.screen = screen
        self.coor = coor
        self.limit_temp = limit_temp
        self.limit_val = limit_val
        self.limit_press = limit_press
        self.term = pygame.image.load('images/temp3.jpg')
        self.snow1 = pygame.image.load('images/snow1.jpg')
        self.snow2 = pygame.image.load('images/snow2.jpg')
        self.fire = pygame.image.load('images/fire.JPG')
        self.gas = pygame.image.load('images/gas.jpg')
        self.my_font = pygame.font.Font('images/Roboto-Black.ttf',
                                        round(0.04 * min(coor[2], coor[3])))
        self.sand = pygame.image.load('images/sand.jpg')
        self.sand_d = pygame.image.load('images/sand_dinamic.jpg')
        self.sand_off = pygame.image.load('images/sand_off.jpg')
        self.backet = pygame.image.load('images/backet.png')
        self.temp_sn = 0
        self.temp_f = 0
        self.k = 1
        self.count_step = round(0.025 * self.coor[2])

    def reinit(self, coor, limit_temp, limit_val, limit_press, screen):
        self.screen = screen
        self.coor = coor
        self.limit_temp = limit_temp
        self.limit_val = limit_val
        self.limit_press = limit_press
        self.my_font = pygame.font.Font('images/Roboto-Black.ttf',
                                        round(0.04 * min(coor[2], coor[3])))
        self.temp_sn = 0
        self.temp_f = 0
        self.k = 1
        self.count_step = round(0.025 * self.coor[2])

    def draw(self, temp, vol, press, mode_press, mode_temp):
        """
        :param temp: текущая температура
        :param vol: текущий объем
        :param press: текущее давление
        :param mode_press: может принимать значения -1, 0, 1.
            Если -1, то изображение высыпания песка,
            если 0, то статичная картинка,
            если 1, то изображение насыпания песка
        :param mode_temp: может принимать значения -1, 0, 1.
            Если -1, то изображение охлаждения,
            если 0, то статичная картинка,
            если 1, то изображение нагрева
        """
        if temp < self.limit_temp[0] or temp > self.limit_temp[1]:
            print(self.limit_temp[0], temp, self.limit_temp[1])
            raise ValueError("Temperature_invalid")
        if vol < self.limit_val[0] or vol > self.limit_val[1]:
            raise ValueError("Value_invalid")
        if press < self.limit_press[0] or press > self.limit_press[1]:
            print(self.limit_press[0], press, self.limit_press[1])
            raise ValueError("Press_invalid")
        if mode_press not in {-1, 0, 1} or mode_temp not in {-1, 0, 1}:
            raise ValueError("Mode_invalid")
        pygame.draw.rect(self.screen, (0, 0, 0), self.coor)
        pygame.draw.rect(self.screen, (255, 255, 255), (self.coor[0] + 2, self.coor[1] + 2, self.coor[2] - 4, self.coor[3] - 4))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (self.coor[0] + round(0.7 * self.coor[2]),
                          self.coor[1],
                          2, self.coor[3]))
        height_piston = round(0.6 * self.coor[3])
        width_piston = round(0.45 * self.coor[2])
        piston_coor = (self.coor[0] + round(0.125 * self.coor[2]),
                       self.coor[1] + round(0.2 * self.coor[3]),
                       width_piston, height_piston)
        pygame.draw.rect(self.screen, (70, 70, 70), piston_coor,
                         round(0.02 * min(self.coor[2], self.coor[3])))
        pygame.draw.rect(self.screen,
                         (255, 255, 255),
                         (self.coor[0] + round(0.125 * self.coor[2]) +
                          round(0.02 * min(self.coor[2], self.coor[3])),
                          self.coor[1] + round(0.2 * self.coor[3]),
                          width_piston - 2 * round(0.02 * min(self.coor[2],
                                                              self.coor[3])),
                          round(0.02 * min(self.coor[2], self.coor[3]))))
        # begin_temp
        term = pygame.transform.scale(self.term,
                                      (round(0.3 * width_piston),
                                       height_piston))
        self.screen.blit(term, (self.coor[0] + round(0.75 * self.coor[2]),
                                self.coor[1] + round(0.2 * self.coor[3])))
        temp_part = (temp - self.limit_temp[0]) / (
                    self.limit_temp[1] - self.limit_temp[0])
        pygame.draw.rect(self.screen, (204, 1, 2),
                         (self.coor[0] + round(0.8034 * self.coor[2]),
                          self.coor[1] + round(
                              (0.28 + 0.42 * (1 - temp_part)) * self.coor[3]),
                          round(0.0279 * self.coor[2]),
                          round((0.42 * temp_part + 0.03) * self.coor[3])))
        if mode_temp == -1:
            snow1 = pygame.transform.scale(self.snow1,
                                           (round(0.09 * self.coor[2]),
                                            height_piston))
            snow2 = pygame.transform.scale(self.snow2,
                                           (round(0.09 * self.coor[2]),
                                            height_piston))
            if self.temp_sn == 0:
                self.screen.blit(snow1,
                                 (self.coor[0] + round(0.0175 * self.coor[2]),
                                  self.coor[1] + round(0.2 * self.coor[3])))
                self.screen.blit(snow2,
                                 (self.coor[0] + round(0.5925 * self.coor[2]),
                                  self.coor[1] + round(0.2 * self.coor[3])))
            else:
                self.screen.blit(snow2,
                                 (self.coor[0] + round(0.0175 * self.coor[2]),
                                  self.coor[1] + round(0.2 * self.coor[3])))
                self.screen.blit(snow1,
                                 (self.coor[0] + round(0.5925 * self.coor[2]),
                                  self.coor[1] + round(0.2 * self.coor[3])))
            self.temp_sn = (self.temp_sn + 1) % 2
        if mode_temp == 1:
            fire = pygame.transform.scale(self.fire, (width_piston,
                                                      round(0.15 * self.coor[
                                                          3])))
            self.screen.blit(fire, (
            self.coor[0] + round(0.125 * self.coor[2]) + self.temp_f,
            self.coor[1] + round(0.825 * self.coor[3])))
            self.temp_f += self.k
            if abs(self.temp_f) == self.count_step:
                self.k *= -1
        for t in range(11):
            if t % 2 == 1:
                continue
            text_surface = self.my_font.render(str(round(self.limit_temp[0] +
                                                         (self.limit_temp[1] -
                                                          self.limit_temp[0]) *
                                                         t / 10)) + ' K',
                                               True, 'Black')
            self.screen.blit(text_surface,
                             (self.coor[0] + round(0.85 * self.coor[2]),
                              self.coor[1] + round((0.675 - t * 0.042) *
                                                   self.coor[3])))
        # end_temp
        # begin_val
        val_part = (vol - self.limit_val[0]) / (
                    self.limit_val[1] - self.limit_val[0])
        x = self.coor[0] + round(0.125 * self.coor[2]) + round(
            0.02 * min(self.coor[2],
                       self.coor[3]))
        gamma = 0.4 * self.coor[3] - 2 * round(
            0.02 * min(self.coor[2], self.coor[3]))
        offset = gamma - gamma * val_part
        y = self.coor[1] + round(0.3 * self.coor[3]) + round(offset)

        pygame.draw.rect(self.screen, (70, 70, 70),
                         (x, y, width_piston - 2 * round(0.02 *
                                                         min(self.coor[2],
                                                             self.coor[3])),
                          round(0.02 * min(self.coor[2], self.coor[3]))))

        gas = pygame.transform.scale(self.gas,
                                     (width_piston - 2 * round(0.02 *
                                                               min(
                                                                self.coor[2],
                                                                self.coor[3])),
                                      round(
                                          self.coor[3] * 0.5 - 2 * round(0.02 *
                                   min(self.coor[2], self.coor[3])) - offset)))
        self.screen.blit(gas, (
        self.coor[0] + round(0.125 * self.coor[2]) + round(
            0.02 * min(self.coor[2], self.coor[3])),
        self.coor[1] + round(0.3 * self.coor[3]) + round(
            0.02 * min(self.coor[2],
                       self.coor[3])) + round(offset)))
        pygame.draw.rect(self.screen, (114, 157, 224),
                         (self.coor[0] + round(0.125 * self.coor[2]) + round(
                             0.02 * min(self.coor[2],
                                        self.coor[3])),
                          self.coor[1] + round(0.3 * self.coor[3]) + round(
                              0.02 * min(self.coor[2],
                                         self.coor[3])) + round(offset),
                          width_piston - 2 * round(
                              0.02 * min(self.coor[2], self.coor[3])),
                          round(self.coor[3] * 0.5 - 2 * round(
                              0.02 * min(self.coor[2],
                                         self.coor[3])) - offset)))
        # end_val
        # begin_press
        press_part = (press - self.limit_press[0]) / (
                    self.limit_press[1] - self.limit_press[0])

        sand_d = pygame.transform.scale(self.sand_d,
                                        (width_piston - 2 * round(
                                            0.02 * min(self.coor[2],
                                                       self.coor[3])),
                                         round(0.3 * self.coor[3]) - 2 + round(
                                             offset)))
        if mode_press == 1:
            self.screen.blit(sand_d, (
            self.coor[0] + round(0.125 * self.coor[2]) + round(
                0.02 * min(self.coor[2],
                           self.coor[3])),
            self.coor[1] + 2))
            sand = pygame.transform.scale(self.sand, (
                width_piston - 2 * round(
                    0.02 * min(self.coor[2], self.coor[3])),
                round(0.1 * self.coor[3] * press_part)))
            self.screen.blit(sand, (
            self.coor[0] + round(0.125 * self.coor[2]) + round(
                0.02 * min(self.coor[2],
                           self.coor[3])),
            self.coor[1] + round(0.3 * self.coor[3]) -
            round(0.1 * self.coor[3] * press_part) + round(offset)))
        if mode_press == 0:
            sand = pygame.transform.scale(self.sand,
                                          (width_piston - 2 * round(
                                              0.02 * min(self.coor[2],
                                                         self.coor[3])),
                                           round(0.1 * self.coor[
                                               3] * press_part)))
            self.screen.blit(sand,
                             (self.coor[0] + round(
                                 0.125 * self.coor[2]) + round(
                                 0.02 * min(self.coor[2], self.coor[3])),
                              self.coor[1] + round(0.3 * self.coor[3]) - round(
                                  0.1 * self.coor[3] *
                                  press_part) + round(offset)))
        if mode_press == -1:
            sand_off = pygame.transform.scale(self.sand_off,
                                              (round(0.48125 * self.coor[2]),
                                               round(0.1 * self.coor[
                                                   3] * press_part)))
            self.screen.blit(sand_off, (
            self.coor[0] + round(0.125 * self.coor[2]) + round(0.02 *
                                           min(self.coor[2], self.coor[3])),
            self.coor[1] + round(0.3 * self.coor[3]) - round(0.1 *
                                                             self.coor[3] *
                                                             press_part) +
                                                                round(offset)))

            backet = pygame.transform.scale(self.backet,
                                            (round(0.0625 * self.coor[2]),
                                             round(0.0625 * self.coor[2])))
            self.screen.blit(backet, (
            self.coor[0] + round(0.575 * self.coor[2]), self.coor[1] +
            round(0.3 * self.coor[3]) + round(offset)))
        # end_press
        pygame.draw.rect(self.screen, (70, 70, 70),
                         (self.coor[0] + round(0.125 *
                                               self.coor[2]) + round(
                             0.02 * min(self.coor[2],
                                        self.coor[3])),
                          self.coor[1] + round(0.3 * self.coor[3]) -
                          round(0.02 * min(self.coor[2], self.coor[3])),
                          round(0.02 * min(self.coor[2], self.coor[3])),
                          round(0.02 * min(self.coor[2], self.coor[3]))))
        if mode_press != -1:
            pygame.draw.rect(self.screen, (70, 70, 70), (
                self.coor[0] + round(
                    0.125 * self.coor[2]) + width_piston - 2 * round(0.02 *
                                            min(self.coor[2], self.coor[3])),
                self.coor[1] + round(0.3 * self.coor[3]) -
                round(0.02 * min(self.coor[2], self.coor[3])),
                round(0.02 * min(self.coor[2], self.coor[3])),
                round(0.02 * min(self.coor[2], self.coor[3]))))
        pygame.display.update()
