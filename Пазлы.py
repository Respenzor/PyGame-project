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

    intro_text = ["Играть",
                  "Правила",
                  "Настройки"]
    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
    window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
