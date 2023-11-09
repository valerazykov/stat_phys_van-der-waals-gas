import pygame

class Info:
    def __init__(self, coor, screen, init_energy):
        """

        :param coor: кортеж из 4 значений: х координата левого верхнего угла,
            у координата левого верхнего угла, ширина области, высота области
        :param screen: объект экрана
        :param init_energy: начальное значение внутренней энергии
        """
        self.screen = screen
        self.coor = coor
        self.my_font = pygame.font.Font('images/Roboto-Black.ttf',
                                        round(0.04 * min(coor[2], coor[3])))
        self.my_font2 = pygame.font.Font('images/Roboto-Black.ttf',
                                        round(0.08 * min(coor[2], coor[3])))
        self.steps = 200
        self.old_data = 0
        self.curr_data = init_energy
        self.ind = 0
        self.old_c = (
            self.coor[0] + round(0.55 * self.coor[2]) - round(
                0.45 * self.coor[2]),
            self.coor[1] + round(0.9 * self.coor[3]),
            round(0.35 * self.coor[2]),
            2)
        self.size = 1

    def reinit(self, coor, screen, init_energy):
        self.screen = screen
        self.coor = coor
        self.steps = 200
        self.old_data = 0
        self.curr_data = init_energy
        self.ind = 0
        self.old_c = (
            self.coor[0] + round(0.55 * self.coor[2]) - round(
                0.45 * self.coor[2]),
            self.coor[1] + round(0.9 * self.coor[3]),
            round(0.35 * self.coor[2]),
            2)
        self.size = 1

    def lines(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (
            self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
            self.coor[1] + round(0.3 * self.coor[3]) - 2,
            round(0.35 * self.coor[2]),
            2))
        pygame.draw.rect(self.screen, (0, 0, 0), (
            self.coor[0] + round(0.55 * self.coor[2]),
            self.coor[1] + round(0.3 * self.coor[3]) - 2,
            round(0.35 * self.coor[2]),
            2))
        pygame.draw.rect(self.screen, (0, 0, 0), (
            self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
            self.coor[1] + round(0.9 * self.coor[3]),
            round(0.35 * self.coor[2]),
            2))
        pygame.draw.rect(self.screen, (0, 0, 0), (
            self.coor[0] + round(0.55 * self.coor[2]),
            self.coor[1] + round(0.9 * self.coor[3]),
            round(0.35 * self.coor[2]),
            2))

    def draw(self, flag, work, energy, warm, step, switch):
        """

        :param work: работа на итерации
        :param energy: изменение внутренней энергии
        :param warm: полученное или отданное количество теплоты
        :param step: номер шага отрисовки (от 0 до 199 включительно)
        :по умолчанию считается, что функция от step = 199 вызовется 1 раз, если нужно более 1 раза,
        то last_draw_for_199 = False, но последний раз обязательно нужно вызвать last_draw_for_199 = True!!!
        Иначе значения не сохранятся
        """
        if switch == True:
            self.old_data = self.curr_data
            self.curr_data += energy
            return
        pygame.draw.rect(self.screen, (255, 255, 255), self.coor)
        for_204 = round((255 - 204) / 200)
        for_255 = round(255 / 200)
        for_128 = round(127 / 200)
        if work > 0:
            pygame.draw.rect(self.screen, (255 - step * for_255, 255 - step * for_204, 255 - step * for_255),
                             (self.coor[0], self.coor[1], round(self.coor[2] / 2), round(self.coor[3] / 5)))
        if work < 0:
            pygame.draw.rect(self.screen, (255, 255 - step * for_255, 255 - step * for_255),
                             (self.coor[0], self.coor[1], round(self.coor[2] / 2), round(self.coor[3] / 5)))
        if warm > 0:
            pygame.draw.rect(self.screen, (255, 255 - step * for_255, 255 - step * for_255),
                             (self.coor[0] + round(self.coor[2] / 2), self.coor[1], round(self.coor[2] / 2), round(self.coor[3] / 5)))
        if warm < 0:
            pygame.draw.rect(self.screen, (255 - step * for_255, 255 - step * for_128, 255),
                             (self.coor[0] + round(self.coor[2] / 2), self.coor[1], round(self.coor[2] / 2), round(self.coor[3] / 5)))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (self.coor[0], self.coor[1] + round(self.coor[3] / 5), self.coor[2], 2))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (self.coor[0] + round(self.coor[2] / 2), self.coor[1], 2, round(self.coor[3] / 5)))
        text_surface = self.my_font.render('Совершённая работа',True, 'Black')
        self.screen.blit(text_surface, (self.coor[0] + round(1 / 11 * self.coor[2]), self.coor[1] + round(1 / 32 * self.coor[3])))
        text_surface = self.my_font.render('Получ./отд. кол-во теплоты', True, 'Black')
        self.screen.blit(text_surface, (self.coor[0] + round(0.54 * self.coor[2]), self.coor[1] + round(1 / 32 * self.coor[3])))
        text_surface = self.my_font2.render(str(work) + ' ДЖ', True, 'Black')
        self.screen.blit(text_surface, (self.coor[0] + round(1 / 7 * self.coor[2]), self.coor[1] + round(1 / 11 * self.coor[3])))
        text_surface = self.my_font2.render(str(warm) + ' ДЖ', True, 'Black')
        self.screen.blit(text_surface,
                         (self.coor[0] + round((0.5 + 1 / 7) * self.coor[2]), self.coor[1] + round(1 / 11 * self.coor[3])))
        text_surface = self.my_font.render('Внутр. энергия на пред. шаге', True, 'Black')
        self.screen.blit(text_surface, (
            self.coor[0] + round(0.05 * self.coor[2]), self.coor[1] + round(0.93 * self.coor[3])))
        text_surface = self.my_font.render('Текущ. внутр. энергия', True, 'Black')
        self.screen.blit(text_surface, (
            self.coor[0] + round(0.55 * self.coor[2]), self.coor[1] + round(0.93 * self.coor[3])))

        if flag <= 200:
            step = step // 4
            step += 150
            if step < 100:
                self.lines()
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2] / 100 * step), self.coor[1] + round(0.3 * self.coor[3]),
                    round(0.35 * self.coor[2]),
                    round(0.6 * self.coor[3])))
                text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.65 * self.coor[2]) - round(0.45 * self.coor[2] / 100 * step), self.coor[1] + round(0.5 * self.coor[3])))

            if step >= 100 and step < 150:
                if energy <= 0:
                    self.lines()
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3])))
                    text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                    self.screen.blit(text_surface, (
                        self.coor[0] + round(0.2 * self.coor[2]),
                        self.coor[1] + round(0.5 * self.coor[3])))
                    pygame.display.update()
                    return
                self.lines()
                new_h = round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy))
                new_h = round(0.6 * self.coor[3]) - new_h
                one_step = round(new_h / 50)
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                    self.coor[1] + round(0.3 * self.coor[3]) + one_step * (step - 100),
                    round(0.35 * self.coor[2]),
                    round(0.6 * self.coor[3]) - one_step * (step - 100)))
                text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.2 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))
            if step >= 150:
                self.lines()
                s = 174 - step
                s += 175
                self.size = round(0.6 * self.coor[3])
                if energy <= 0:
                    self.size = (1 + energy / self.curr_data) * 0.6 * self.coor[3]
                    text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                    self.screen.blit(text_surface, (
                        self.coor[0] + round(0.2 * self.coor[2]),
                        self.coor[1] + round(0.5 * self.coor[3])))
                    self.old_c = (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(
                            0.45 * self.coor[2]),
                        self.coor[1] + round(0.9 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        2)
                else:

                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(
                            self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy)),
                        round(0.35 * self.coor[2]),
                        round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy))))
                    text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                    self.screen.blit(text_surface, (
                        self.coor[0] + round(0.2 * self.coor[2]),
                        self.coor[1] + round(0.5 * self.coor[3])))
                    self.old_c = (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(
                            0.45 * self.coor[2]),
                        self.coor[1] + round(0.9 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        2)
                color = (0, 204, 0)
                if energy < 0:
                    color = (255, 128, 0)
                pygame.draw.rect(self.screen, color, (
                    self.coor[0] + round(0.55 * self.coor[2]),
                    self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(self.size) + round(
                        self.size / 50 * (s - 150)), round(0.35 * self.coor[2]),
                    round(self.size) - round(self.size / 50 * (s - 150))))
                if round(self.size) - round(self.size / 50 * (s - 150)) < self.old_c[3]:
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(self.size) + round(
                            self.size / 50 * (s - 150)), round(0.35 * self.coor[2]),
                        round(self.size) - round(self.size / 50 * (s - 150))))
                else:
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - self.old_c[3],
                        round(0.35 * self.coor[2]),
                        self.old_c[3]))
                if step == 199 and energy < 0:
                    pygame.draw.rect(self.screen, (255, 0, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3]) - round(self.size)))
                if energy < 0:
                    text_surface = self.my_font.render(str(self.curr_data) + str(energy) + ' ДЖ', True, 'Black')
                elif energy > 0:
                    text_surface = self.my_font.render(str(self.curr_data) + ' + ' + str(energy) + ' ДЖ', True, 'Black')
                else:
                    text_surface = self.my_font.render(
                        str(self.curr_data) + ' ДЖ', True,
                        'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.65 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))
                if switch == True:
                    self.old_data = self.curr_data
                    self.curr_data += energy
        if flag > 200:
            if step < 50:
                self.lines()
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.old_c[0], self.coor[1] + round(0.9 * self.coor[3]) - round(self.old_c[3]) + round(self.old_c[3] / 50 * step),
                    self.old_c[2],
                    round(self.old_c[3] / 50 * (50 - step))))
                text_surface = self.my_font.render(str(self.curr_data)  + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.65 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.coor[0] + round(0.55 * self.coor[2]),
                    self.coor[1] + round(0.9 * self.coor[3]) - round(self.size),
                    round(0.35 * self.coor[2]),
                    round(self.size)))
                if round(self.size) != round(0.6 * self.coor[3]):
                    pygame.draw.rect(self.screen, (255, 0, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3]) - round(self.size)))
                else:
                    pygame.draw.rect(self.screen, (0, 204, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3]) - self.old_c[3]))
                text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.65 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))
            if step >= 50 and step < 100:
                self.lines()
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2] / 50 * (step - 50)), self.coor[1] + round(0.9 * self.coor[3]) - round(self.size),
                    round(0.35 * self.coor[2]),
                    round(self.size)))
                text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.65 * self.coor[2]) - round(0.45 * self.coor[2] / 50 * (step - 50)),
                    self.coor[1] + round(0.5 * self.coor[3])))
            if step >= 100 and step < 125:
                self.lines()
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.coor[0] + round(0.1 * self.coor[2]),
                    self.coor[1] + round(0.9 * self.coor[3]) - round(self.size) - (round(self.size) + round((0.6 * self.coor[3] - self.size) / 25 * (step - 100)) - round(self.size)),
                    round(0.35 * self.coor[2]),
                    round(self.size) + round((0.6 * self.coor[3] - self.size) / 25 * (step - 100))))
                text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.2 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))
            if step >= 125 and step < 150:
                self.lines()
                if energy <= 0:
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3])))
                    text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                    self.screen.blit(text_surface, (
                        self.coor[0] + round(0.2 * self.coor[2]),
                        self.coor[1] + round(0.5 * self.coor[3])))
                    return

                new_h = round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy))
                new_h = round(0.6 * self.coor[3]) - new_h
                one_step = round(new_h / 50)
                pygame.draw.rect(self.screen, (255, 128, 0), (
                    self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                    self.coor[1] + round(0.3 * self.coor[3]) + one_step * (step - 100),
                    round(0.35 * self.coor[2]),
                    round(0.6 * self.coor[3]) - one_step * (step - 100)))
                text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.2 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))
            if step >= 150:
                self.lines()
                s = 174 - step
                s += 175
                self.size = round(0.6 * self.coor[3])
                if energy <= 0:
                    self.size = (1 + energy/ self.curr_data) * 0.6 * self.coor[3]
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3])))
                    text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                    self.screen.blit(text_surface, (
                        self.coor[0] + round(0.2 * self.coor[2]),
                        self.coor[1] + round(0.5 * self.coor[3])))
                    self.old_c = (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3]))
                else:

                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy)),
                        round(0.35 * self.coor[2]),
                        round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy))))
                    text_surface = self.my_font.render(str(self.curr_data) + ' ДЖ', True, 'Black')
                    self.screen.blit(text_surface, (
                        self.coor[0] + round(0.2 * self.coor[2]),
                        self.coor[1] + round(0.5 * self.coor[3])))
                    self.old_c = (
                        self.coor[0] + round(0.55 * self.coor[2]) - round(0.45 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy)),
                        round(0.35 * self.coor[2]),
                        round(self.curr_data * 0.6 * self.coor[3] / (self.curr_data + energy)))
                color = (0, 204, 0)
                if energy < 0:
                    color = (255, 128, 0)
                pygame.draw.rect(self.screen, color, (
                        self.coor[0] + round(0.55 * self.coor[2]), self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(self.size)+round(self.size / 50 * (s - 150)), round(0.35 * self.coor[2]),
                        round(self.size) - round(self.size / 50 * (s - 150))))
                if round(self.size) - round(self.size / 50 * (s - 150)) < self.old_c[3]:
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - round(self.size) + round(
                            self.size / 50 * (s - 150)), round(0.35 * self.coor[2]),
                        round(self.size) - round(self.size / 50 * (s - 150))))
                else:
                    pygame.draw.rect(self.screen, (255, 128, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]) + round(0.6 * self.coor[3]) - self.old_c[3], round(0.35 * self.coor[2]),
                        self.old_c[3]))
                if step == 199 and energy < 0:
                    pygame.draw.rect(self.screen, (255, 0, 0), (
                        self.coor[0] + round(0.55 * self.coor[2]),
                        self.coor[1] + round(0.3 * self.coor[3]),
                        round(0.35 * self.coor[2]),
                        round(0.6 * self.coor[3]) - round(self.size)))
                if energy < 0:
                    text_surface = self.my_font.render(str(self.curr_data) + str(energy) + ' ДЖ', True, 'Black')
                else:
                    text_surface = self.my_font.render(str(self.curr_data) + ' + ' + str(energy) + ' ДЖ', True, 'Black')
                self.screen.blit(text_surface, (
                    self.coor[0] + round(0.65 * self.coor[2]),
                    self.coor[1] + round(0.5 * self.coor[3])))


                if switch == True:
                    self.old_data = self.curr_data
                    self.curr_data += energy
        pygame.display.update()

class Info_smart:
    def __init__(self, coor, screen, init_energy):
        self.iter = 0
        self.work = 0
        self.warm = 0
        self.energy = 0
        self.coor = (coor[0], coor[1], coor[2], coor[3])
        self.screen = screen
        self.inf = Info(coor, screen, init_energy)

    def reinit(self, coor, screen, init_energy):
        self.iter = 0
        self.work = 0
        self.warm = 0
        self.energy = 0
        self.coor = (coor[0], coor[1], coor[2], coor[3])
        self.screen = screen
        self.inf.reinit(coor, screen, init_energy)

    def next_iteration(self, work, energy, warm):
        self.iter += 1
        self.work = work
        self.warm = warm

        self.inf.draw(150, self.work, self.energy, self.warm, 7, True)
        self.energy = energy
    def take_picture(self, step):
        if self.iter == 0:
            self.inf.draw(150, self.work, self.energy, self.warm, step, False)
        else:
            self.inf.draw(250, self.work, self.energy, self.warm, step, False)

pygame.init()
scr = pygame.display.set_mode((1700, 1000))
pygame.display.set_caption("Our statphis2")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
#pygame.draw.rect(self.screen, (0, 0, 0), (self.coor[0] + round(0.1 * self.coor[2]), self.coor[1] + round(0.9 * self.coor[3]), round(0.35 * self.coor[2]), 2))
#        pygame.draw.rect(self.screen, (0, 0, 0), (
#        self.coor[0] + round(0.55 * self.coor[2]), self.coor[1] + round(0.3 * self.coor[3]), round(0.35 * self.coor[2]),
#        round(0.6 * self.coor[3])))

running = True
if running:
    scr.fill((114, 157, 224))
    inf = Info_smart((0, 0, 800, 600), scr, 80)

    for s in range(200):
        pygame.time.wait(50)
        inf.take_picture(s)
    inf.next_iteration(300, -20, -12)
    for s in range(200):
        pygame.time.wait(50)
        inf.take_picture(s)
    inf.next_iteration(-350, 190, 12)

    for s in range(200):
        pygame.time.wait(50)
        inf.take_picture(s)
    inf.next_iteration(-350, -190, 12)

    for s in range(200):
        pygame.time.wait(50)
        inf.take_picture(s)
    inf.next_iteration(-350, -9, 12)
    while 1:
        u = 9
