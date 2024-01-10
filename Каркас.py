import pygame
pygame.init()

W, H = 800, 800
FPS = 60
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

def start_screen():
    print('Вызвана функция запуска меню игры')

if __name__ == '__main__':
    start_screen()
