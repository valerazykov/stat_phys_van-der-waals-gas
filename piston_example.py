import pygame
from piston import Piston


pygame.init()
scr = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Our statphis")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

running = True
piston = Piston((0, 0, 1000, 700), (200, 300), (100, 400), (200, 300), scr)
scr.fill((114, 157, 224))
while running:

    for t in range(100):
        pygame.time.wait(10)
        piston.draw(200 + t, 100, 300, 0, 1)
    for t in range(100):
        pygame.time.wait(10)
        piston.draw(300 - t, 100, 300, 0, -1)
    for v in range(300):
        pygame.time.wait(10)
        piston.draw(200, 100 + v, 300, 0, 0)
    for v in range(300):
        pygame.time.wait(10)
        piston.draw(200, 400 - v, 300, 0, 0)
    for v in range(300):
        pygame.time.wait(10)
        piston.draw(200, 100 + v, 300, 0, 0)
    for p in range(100):
        pygame.time.wait(30)
        piston.draw(200, 400, 300 - p, -1, 0)

    for p in range(100):
        pygame.time.wait(30)
        piston.draw(200, 400, 200 + p, 1, 0)
    for p in range(100):
        pygame.time.wait(30)
        piston.draw(200, 400, 300 - p, -1, 0)
    for t in range(100):
        pygame.time.wait(10)
        piston.draw(200 + t, 100, 300, 0, 1)
    for t in range(100):
        pygame.time.wait(10)
        piston.draw(300 - t, 100, 300, 0, -1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False