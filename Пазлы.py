import pygame
from utils import load_image
pygame.init()

W, H = 800, 800
FPS = 60

window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    fon = pygame.transform.scale(load_image('fon.jpg'), (W, H))
    window.blit(fon, (0, 0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
