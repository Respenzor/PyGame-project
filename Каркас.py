import pygame
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

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
