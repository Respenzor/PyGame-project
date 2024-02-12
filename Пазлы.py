import pygame
import sys

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
GAME_NAME = 'Magick Puzzles'
BUTTON_IMAGE = 'knopka.png'
BUTTON_ACTIVE_IMAGE = 'knopka_active.png'
BUTTON_SOUND = 'knopka_press.mp3'
IMAGE = pygame.image.load('level 1.jpeg')
WAIT = 'Загрузка...'

pygame.init()
W_game, H_game = IMAGE.get_width(), IMAGE.get_height()
pygame.display.set_caption(GAME_NAME)
W, H = 1920, 1080
FPS = 60
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


def main():
    global board
    start_screen(window, clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                cell = board.get_cell(mouse_pos)
                if cell:
                    board.on_click(cell)

        clock.tick(FPS)


def start_screen(window, clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND):
    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
    font = pygame.font.Font(None, 125)
    window.blit(fon, (0, 0))
    pygame.display.flip()

    game_name = font.render(GAME_NAME, True, (255, 255, 255))
    game_name_rect = game_name.get_rect(center=(W // 2, 110))
    window.blit(game_name, game_name_rect)
    pygame.display.flip()

    start_button = Buttons(W // 2 - 250, 225, 500, 200, 'Играть', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    options_button = Buttons(W // 2 - 250, 450, 500, 200, 'Настройки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    quit_button = Buttons(W // 2 - 250, 675, 500, 200, 'Выход', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)

    buttons = [start_button, options_button, quit_button]
    show_menu = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_menu:
                    for button in buttons:
                        button.event(event)
            elif event.type == pygame.USEREVENT:
                if show_menu:
                    if event.button == start_button:
                        pygame.display.set_mode((W_game, H_game))
                        window.fill((0, 0, 0))
                        board = Board(W_game, H_game, IMAGE)
                        board.set_view(0, 0, min(W // board.width, H // board.height))
                        board.create(window)
                        show_menu = False
                    elif event.button == options_button:
                        print('Меню настроек')
                        pygame.display.flip()
                    elif event.button == quit_button:
                        pygame.quit()
                        sys.exit()

        if show_menu:
            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.check_active(mouse_pos)

            for button in buttons:
                button.draw(window)
        else:
            board.create(window)  # Загрузка доски
            board.render(window) #Отрисовка доски
            pygame.display.flip()
            pygame.display.update()
            return

        pygame.display.update()
        clock.tick(FPS)


class Buttons:
    def __init__(self, x, y, width, height, text, image_location, image_actived_location=None, button_actived_location=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image_location = pygame.image.load(image_location)
        self.image_location = pygame.transform.scale(self.image_location, (width, height))
        self.image_actived = self.image_location
        if image_actived_location:
            self.image_actived = pygame.image.load(image_actived_location)
            self.image_actived = pygame.transform.scale(self.image_actived, (width, height))
        self.rect = self.image_location.get_rect(topleft=(x, y))
        self.sound = None
        if button_actived_location:
            self.sound = pygame.mixer.Sound(button_actived_location)
        self.actived = False

    def draw(self, window):
        proverka_knopki = self.image_actived if self.actived else self.image_location
        window.blit(proverka_knopki, self.rect.topleft)
        font = pygame.font.Font(None, 60)
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


class Board:
    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        self.left = 0  # смещение по оси абцисс
        self.top = 0  # смещение по оси ординат
        self.cell_size = 120
        self.image = image
        self.loaded = False
        self.sprite_images = []

    def create(self, window):
        if not self.loaded:
            window.fill((0, 0, 0))
            font = pygame.font.Font(None, 125)
            wait = font.render(WAIT, True, (255, 255, 255))
            wait_rect = wait.get_rect(center=(W_game // 2, H_game // 2))
            window.blit(wait, wait_rect)
            pygame.display.flip()
            sprite_width = self.image.get_width() // self.width
            sprite_height = self.image.get_height() // self.height
            for y in range(self.height):
                sprite_row = []
                for x in range(self.width):
                    sprite_rect = pygame.Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
                    sprite_image = pygame.Surface((sprite_width, sprite_height))
                    sprite_image.blit(self.image, (0, 0), area=sprite_rect)
                    sprite_row.append(sprite_image)
                self.sprite_images.append(sprite_row)
            pygame.display.flip()
            self.loaded = True
    def render(self, window):
        if self.loaded:
            window.fill((0, 0, 0))
            for y in range(self.height):
                for x in range(self.width):
                    cell_left = x * self.cell_size + self.left
                    cell_top = y * self.cell_size + self.top
                    cell_rect = pygame.Rect(cell_left, cell_top, self.cell_size, self.cell_size)
                    pygame.draw.rect(window, pygame.Color(255, 255, 255), cell_rect, 1)
                    cell_image = self.sprite_images[y][x]
                    window.blit(cell_image, (cell_left, cell_top))
            pygame.display.flip()
            pygame.display.update()

    def set_view(self, left, top, cell_size):
        window_width, window_height = pygame.display.get_surface().get_size()
        board_width = self.width * cell_size
        board_height = self.height * cell_size
        left = (window_width - board_width) // 2
        top = (window_height - board_height) // 2
        self.left = left
        self.top = top
        self.cell_size_x = cell_size
        self.cell_size_y = cell_size * self.height / self.width
        self.cell_size = cell_size

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] < self.left + self.width * self.cell_size and self.top <= mouse_pos[1] < self.top + self.height * self.cell_size:
            return (int((mouse_pos[0] - self.left) / self.cell_size), int((mouse_pos[1] - self.top) / self.cell_size))
        else:
            return None


if __name__ == '__main__':
    board = Board(W_game, H_game, IMAGE)
    main()
