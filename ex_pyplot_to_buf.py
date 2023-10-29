import matplotlib.pyplot as plt
import numpy as np
import pygame
import io

x = np.linspace(0, 10, 100)
funcs = [np.sin, np.cos, np.log, np. exp]
y_labels = ["sin", "cos", "log", "exp"]
plot_surfaces = []

for i in range(4):
    plt.plot(x, np.sin(x))
    plt.xlabel('итерация')
    plt.ylabel(y_labels[i])
    plot_stream = io.BytesIO()
    plt.savefig(plot_stream)
    plot_stream.seek(0)
    plot_surfaces.append(pygame.image.load(plot_stream))


pygame.init()

info_obj = pygame.display.Info()
width = info_obj.current_w * 0.7
height = info_obj.current_h * 0.9
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(0)

    window.blit(plot_surfaces[0], (0, 0))
    window.blit(plot_surfaces[1], (width // 2, 0))
    window.blit(plot_surfaces[2], (0, height // 2))
    window.blit(plot_surfaces[3], (width // 2, height // 2))

    pygame.display.flip()

pygame.quit()
exit()