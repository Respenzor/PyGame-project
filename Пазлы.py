import pygame
import sys
import random
import sqlite3

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
EMPTY = pygame.image.load('empty_cell.png')

pygame.init()
W_game, H_game = 1920, 1000
pygame.display.set_caption(GAME_NAME)
W, H = 1920, 1080
FPS = 60
sprites = []
coords_rand = []
game_finish = []
game_sprites = []
empty_sprite = pygame.sprite.Group()
sprites_group = pygame.sprite.Group()
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


class Empty_sprite(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(empty_sprite)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x - 248, pos_y - 248)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(sprites_group)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


empty_cell = Empty_sprite(EMPTY, 1500, 1000)
empty_sprite.add(empty_cell)

def main():
    board = Board(W_game, H_game, IMAGE)
    start_screen(window, clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND, board)
    running = True
    game_events = Game_events(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                cell = board.get_cell(mouse_pos)
                if cell:
                    board.on_click(cell)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_events.move_up()
                elif event.key == pygame.K_DOWN:
                    game_events.move_down()
                elif event.key == pygame.K_LEFT:
                    game_events.move_left()
                elif event.key == pygame.K_RIGHT:
                    game_events.move_right()

        clock.tick(FPS)


def start_screen(window, clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND, board):
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
                    if event.button.text == 'Играть':
                        pygame.display.set_mode((W_game, H_game))
                        window.fill((0, 0, 0))
                        board.set_view(250)
                        board.create(window)
                        show_menu = False
                    elif event.button.text == 'Настройки':
                        print('Меню настроек')
                        pygame.display.flip()
                    elif event.button.text == 'Выход':
                        pygame.quit()
                        sys.exit()

        if show_menu:
            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.check_active(mouse_pos)

            for button in buttons:
                button.draw(window)
        else:
            board.render(window)  # Отрисовка доски
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
        self.left = 0
        self.top = 0
        self.cell_size = 250
        self.image = image
        self.loaded = False
        self.image_board = None
        self.show_sprites = True

    def create(self, window):
        if not self.loaded:
            window.fill((0, 0, 0))
            font = pygame.font.Font(None, 125)
            wait = font.render(WAIT, True, (255, 255, 255))
            wait_rect = wait.get_rect(center=(W_game // 2, H_game // 2))
            window.blit(wait, wait_rect)
            pygame.display.flip()
            sprites_cl = Image_sprites(IMAGE.get_width(), IMAGE.get_height(), IMAGE)
            sprites_cl.split()
            for sprite, (x, y) in sprites[0:-1]:
                coords_rand.append((x, y))
            random.shuffle(coords_rand)
            self.loaded = True

    def render(self, window):
        count = 0
        if self.loaded:
            window.fill((0, 0, 0))
            for y in range(1000):
                for x in range(1500):
                    cell_left = x * self.cell_size + self.left
                    cell_top = (self.height - y) * self.cell_size + self.top
                    pygame.draw.rect(window, pygame.Color(255, 255, 255), (cell_left, cell_top, self.cell_size, self.cell_size), 2)
            pygame.draw.rect(window, (0, 0, 0), (1501, 0, 1000, 1500))
        if self.show_sprites:
            for sprite, (x, y) in sprites[0:-1]:
                x_rand, y_rand = coords_rand[count]
                count += 1
                self.sprite_game = Sprite(sprite, x_rand, y_rand)
                sprites_group.add(self.sprite_game)
                game_sprites.append((sprite, (x_rand, y_rand)))
            sprites_group.draw(window)
            empty_sprite.draw(window)
        else:
            sprites_group.draw(window)
            empty_sprite.draw(window)
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, 0, 2, H_game))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(W_game - 2, 0, 2, H_game))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, 0, W_game, 2))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, H_game - 2, W_game, 2))
        pygame.display.flip()
        pygame.display.update()



    def set_view(self, cell_size):
        window_width, window_height = 1500, 1000
        board_width = self.width * cell_size
        board_height = self.height * cell_size
        left = (window_width - board_width) // 2 - self.left
        top = (window_height - board_height) // 2 - self.top
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] < self.left + self.width * self.cell_size and self.top <= mouse_pos[1] < self.top + self.height * self.cell_size:
            return (int((mouse_pos[0] - self.left) // self.cell_size) + 1) // self.cell_size, (int((mouse_pos[1] - self.top) // self.cell_size)) // self.cell_size


class Image_sprites(Board):
    def __init__(self, width, height, image):
        super().__init__(width, height, image)
        self.image = image
        self.cell = self.cell_size
        self.empty_cell_x = 0
        self.empty_cell_y = 0

    def split(self):
        count = 0
        for y in range(0, self.height - self.cell, self.cell):
            for x in range(250, self.width - self.cell + 1, self.cell):
                count += 1
                sprite = self.image.subsurface((x, y, self.cell - 5, self.cell - 5))
                sprites.append((sprite, (x - 248, y + 2)))
                game_finish.append((sprite, (x - 248, y + 2)))


    def return_coordinate(self, cell_coords):
        cell_x, cell_y = cell_coords
        sprite_x = cell_x * self.cell_size
        sprite_y = cell_y * self.cell_size
        for sprite, (x, y) in sprites:
            if sprite_x == x and sprite_y == y:
                return x // self.cell_size, y // self.cell_size


class Game_events(Board):
    def __init__(self, board):
        super().__init__(board.width, board.height, board.image)
        self.board = board
        self.sprite_pose_x = 0
        self.sprite_pose_y = 0

    def move_up(self):
        for empty in empty_sprite:
            empty.rect.y -= 250
            collision = pygame.sprite.spritecollide(empty, sprites_group, False)
            if collision:
                st_x, st_y, end_x, end_y = empty.rect.x, empty.rect.y, empty.rect.x, empty.rect.y
                empty_cell.update(end_x, end_y)
                for sp in collision:
                    sp.update(st_x, st_y + 250)
                    self.show_sprites = False
                    self.render(window)
            else:
                empty.rect.y += 250

    def move_down(self):
        for empty in empty_sprite:
            empty.rect.y += 250
            collision = pygame.sprite.spritecollide(empty, sprites_group, False)
            if collision:
                st_x, st_y, end_x, end_y = empty.rect.x, empty.rect.y, empty.rect.x, empty.rect.y
                empty_cell.update(end_x, end_y)
                for sp in collision:
                    sp.update(st_x, st_y - 250)
                    self.show_sprites = False
                    self.render(window)
            else:
                empty.rect.y -= 250

    def move_left(self):
        for empty in empty_sprite:
            empty.rect.x -= 250
            collision = pygame.sprite.spritecollide(empty, sprites_group, False)
            if collision:
                st_x, st_y, end_x, end_y = empty.rect.x, empty.rect.y, empty.rect.x, empty.rect.y
                empty_cell.update(end_x, end_y)
                for sp in collision:
                    sp.update(st_x + 250, st_y)
                    self.show_sprites = False
                    self.render(window)
            else:
                empty.rect.x += 250

    def move_right(self):
        for empty in empty_sprite:
            empty.rect.x += 250
            collision = pygame.sprite.spritecollide(empty, sprites_group, False)
            if collision:
                st_x, st_y, end_x, end_y = empty.rect.x, empty.rect.y, empty.rect.x, empty.rect.y
                empty_cell.update(end_x, end_y)
                for sp in collision:
                    sp.update(st_x - 250, st_y)
                    self.show_sprites = False
                    self.render(window)
            else:
                empty.rect.x -= 250


if __name__ == '__main__':
    main()