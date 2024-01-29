import pygame
import sys

pygame.init()

W, H = 800, 700
FPS = 60
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

GAME_NAME = 'Magick Puzzles'
BUTTON_IMAGE = 'knopka.png'
BUTTON_ACTIVE_IMAGE = 'knopka_active.png'
BUTTON_SOUND = 'knopka_press.mp3'


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
    font = pygame.font.Font(None, 125)
    window.blit(fon, (0, 0))
    pygame.display.flip()

    game_name = font.render(GAME_NAME, True, (255, 255, 255))
    game_name_rect = game_name.get_rect(center=(W // 2, 110))
    window.blit(game_name, game_name_rect)
    pygame.display.flip()

    start_button = Buttons(250, 225, 300, 100, 'Играть', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    options_button = Buttons(250, 355, 300, 100, 'Настройки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    quit_button = Buttons(250, 475, 300, 100, 'Выход', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    buttons = [start_button, options_button, quit_button]

    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.event(event)

            if event.type == pygame.USEREVENT:
                if event.button == start_button:
                    game_started = True
                    pygame.display.set_mode((1000, 800))
                    window.fill((0, 0, 0))
                elif event.button == options_button:
                    print('Нажата кнопка настроек')
                    # Открытие окна настроек при нажатии на кнопку
                elif event.button == quit_button:
                    pygame.quit()
                    sys.exit()

        if game_started:
            pygame.display.flip()
            game()
            break

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_active(mouse_pos)

        for button in buttons:
            button.draw(window)
        pygame.display.update()
        clock.tick(FPS)


class Buttons:
    def __init__(self, x, y, width, height, text, image_location, image_actived_location=None, button_actived_location=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image_location = pygame.image.load('knopka.png')
        self.image_location = pygame.transform.scale(self.image_location, (width, height))
        self.image_actived = self.image_location
        if image_actived_location:
            self.image_actived = pygame.image.load('knopka_active.png')
            self.image_actived = pygame.transform.scale(self.image_actived, (width, height))
        self.rect = self.image_location.get_rect(topleft=(x, y))
        self.sound = None
        if button_actived_location:
            self.sound = pygame.mixer.Sound(button_actived_location)
        self.actived = False

    def draw(self, window):
        proverka_knopki = self.image_actived if self.actived else self.image_location
        window.blit(proverka_knopki, self.rect.topleft)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (225, 225, 225))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def check_active(self, mouse_pos):
        self.actived = self.rect.collidepoint(mouse_pos)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.actived:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


def game():
    board = Board(W, H)
    board.render()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        self.left = 100 #смещение по оси абцисс
        self.top = 100 #смещение по оси ординат
        self.cell_size = 100 #размер клеток

    def render(self):
        window_width, window_height = window.get_size()
        board_width = self.width * self.cell_size
        board_height = self.height * self.cell_size
        left = (window_width - board_width) // 2
        top = (window_height - board_height) // 2

        for y in range(self.height):
            for x in range(self.width):
                cell_left = x * self.cell_size + left
                cell_top = y * self.cell_size + top
                if cell_left >= 0 and cell_left + self.cell_size <= window_width and cell_top >= 0 and cell_top + self.cell_size <= window_height:
                    pygame.draw.rect(window, pygame.Color(255, 255, 255), (cell_left, cell_top, self.cell_size, self.cell_size), self.board[y][x])
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    cell = self.get_cell(mouse_pos)
                    if cell:
                        self.on_click(cell)

            clock.tick(FPS)

    def set_view(self, left, top, cell_size):
        window_width, window_height = window.get_size()
        board_width = self.width * cell_size
        board_height = self.height * cell_size
        left = (window_width - board_width) // 2
        top = (window_height - board_height) // 2
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] < self.left + self.width * self.cell_size and self.top <= mouse_pos[1] < self.top + self.height * self.cell_size:
            return (int((mouse_pos[0] - self.left) / self.cell_size), int((mouse_pos[1] - self.top) / self.cell_size))
        else:
            return None


if __name__ == '__main__':
    start_screen()