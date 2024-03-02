import pygame
import sys
import random


GAME_NAME = 'Image Puzzles' #Название игры
BUTTON_IMAGE = 'knopka.png' #Изображение кнопки
BUTTON_ACTIVE_IMAGE = 'knopka_active.png' #Изображение кнопки при наведении на неё
BUTTON_SOUND = 'knopka_press.mp3' #Звук нажатия на кнопку
IMAGE = pygame.image.load('level 1.jpeg') #Изображение (игровое поле)
WAIT = 'Загрузка...' #Текст загрузки игры
EMPTY = pygame.image.load('empty_cell.png') #Изображение пустой клетки

#Инициализация
pygame.init()
W_game, H_game = 1920, 1000 #Размеры окна игры
pygame.display.set_caption(GAME_NAME)
W, H = 1920, 1080 #Размеры меню
FPS = 60 #Частота обновления экрана
sprites = [] #Хранение элементов картинки и их координат на клетчатом поле
coords_rand = [] #Координаты элементов картинки
game_finish = pygame.sprite.Group() #Правильное расположение спрайтов на игровом поле
empty_sprite = pygame.sprite.Group() #Пустой спрайт - объект для перемещения
sprites_group = pygame.sprite.Group() #Текущее расположение спрайтов на игровом поле
window = pygame.display.set_mode((W, H)) #Основное окно игры
clock = pygame.time.Clock()


class Buttons: #Обработка событий кнопок
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

    def draw(self, window): #Отрисовка кнопки
        proverka_knopki = self.image_actived if self.actived else self.image_location
        window.blit(proverka_knopki, self.rect.topleft)
        font = pygame.font.Font(None, 60)
        text_surface = font.render(self.text, True, (225, 225, 225))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def check_active(self, mouse_pos): #Проверка наведения на кнопку
        self.actived = self.rect.collidepoint(mouse_pos)

    def event(self, event): #Обработка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.actived:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class Settings: #Меню настроек игры
    def __init__(self):
        self.visible = None

    def draw(self, window):
        if self.visible:
            fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
            window.blit(fon, (0, 0))
            pygame.display.flip()
            sound_button = Buttons(W // 4 + 100, 225, 800, 200, 'Музыка и звуки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            game_settings_button = Buttons(W // 4 + 100, 450, 800, 200, 'Прочее', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            back_button = Buttons(W // 4 + 100, 675, 800, 200, 'Назад', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            buttons = [sound_button, game_settings_button, back_button]

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in buttons:
                            button.check_active(mouse_pos)
                            button.event(event)

                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_active(mouse_pos)

                for button in buttons:
                    button.draw(window)
                pygame.display.update()
                clock.tick(FPS)


class Board:#Игровое поле
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
        self.buttons = [
            Buttons(1502, 350, 414, 175, 'Пауза', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND),
            Buttons(1502, 585, 414, 175, 'Настройки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND),
            Buttons(1502, 820, 414, 175, 'Выход', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)]

    def create(self, window): #Создание игрового поля
        self.loaded = False
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

    def render(self, window): #Отрисовка игрового поля
        count = 0
        if self.loaded:
            window.fill((0, 0, 0))
            for y in range(1000):
                for x in range(1500):
                    cell_left = x * self.cell_size + self.left
                    cell_top = (self.height - y) * self.cell_size + self.top
                    pygame.draw.rect(window, pygame.Color(255, 255, 255), (cell_left, cell_top, self.cell_size, self.cell_size), 2)
            pygame.draw.rect(window, (0, 0, 0), (1501, 0, 1000, 1500))
            window.blit(pygame.transform.scale(IMAGE, (420, 300)), (1501, 2))
        if self.show_sprites:
            for sprite, (x, y) in sprites[0:-1]:
                x_rand, y_rand = coords_rand[count]
                count += 1
                self.sprite_game = Sprite(sprite, x_rand, y_rand, count)
                sprites_group.add(self.sprite_game)
                check = Final(sprite, x, y, count)
                game_finish.add(check)
            sprites_group.draw(window)
            empty_sprite.draw(window)
        else:
            sprites_group.draw(window)
            empty_sprite.draw(window)
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, 0, 2, H_game))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(W_game - 2, 0, 2, H_game))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, 0, W_game, 2))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, H_game - 2, W_game, 2))
        for button in self.buttons:
            button.draw(window)
        pygame.display.flip()
        pygame.display.update()

    def set_view(self, cell_size): #Обработка размеров, смещения: подготовка к созданию игрового окна
        window_width, window_height = 1500, 1000
        board_width = self.width * cell_size
        board_height = self.height * cell_size
        left = (window_width - board_width) // 2 - self.left
        top = (window_height - board_height) // 2 - self.top
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def event(self, event): #Обработка нажатий кнопок игрового окна
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.actived:
                    if button.sound:
                        button.sound.play()
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=button))


class Image_sprites(Board): #Разделение картинки на части, в соответствии клетчатому полю
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


class Game_events(Board): #Перемещение спрайтов по полю
    def __init__(self, board):
        super().__init__(board.width, board.height, board.image)
        self.board = board
        self.sprite_pose_x = 0
        self.sprite_pose_y = 0

    def move_up(self): #Перемещение спрайта, обозначающего пустую клетку вверх, если сверху есть другой спрайт
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
                    return True
            else:
                empty.rect.y += 250

    def move_down(self): #Перемещение спрайта, обозначающего пустую клетку вниз, если снизу есть другой спрайт
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
                    return True
            else:
                empty.rect.y -= 250

    def move_left(self): #Перемещение спрайта, обозначающего пустую клетку влево, если слева есть другой спрайт
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
                    return True
            else:
                empty.rect.x += 250

    def move_right(self): #Перемещение спрайта, обозначающего пустую клетку вправо, если справа есть другой спрайт
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
                    return True
            else:
                empty.rect.x -= 250


class Empty_sprite(pygame.sprite.Sprite): #Создание и обработка перемещения спрайта пустой клетки
    def __init__(self, image, pos_x, pos_y):
        super().__init__(empty_sprite)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x - 248, pos_y - 248)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Sprite(pygame.sprite.Sprite): #Создание и обработка перемещения спрайтов (элементы картинки Image, разделённой в классе Image_sprites)
    def __init__(self, image, pos_x, pos_y, index):
        super().__init__(sprites_group)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.ind = index

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Final(pygame.sprite.Sprite): #Создание спрайтов для проверки правильности сборки, аналогичное, по принципу действия, классу Sprite
    def __init__(self, image, pos_x, pos_y, index):
        super().__init__(game_finish)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.ind = index


def start_screen(clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND, board): #Функция отрисовки стартового окна
    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
    font = pygame.font.Font(None, 125)
    window = pygame.display.set_mode((W, H))
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
                        fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
                        window.blit(fon, (0, 0))
                        pygame.display.flip()
                        settings = Settings()
                        settings.visible = True
                        settings.draw(window)
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
            board.render(window)
            pygame.display.flip()
            pygame.display.update()
            return

        pygame.display.update()
        clock.tick(FPS)


def end_screen(old, new): #Финальное окно игры (итоги)
    buttons = [Buttons(100, 100, 100, 100, 'Выход', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)]
    window = pygame.display.set_mode((700, 400))
    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), window.get_size())
    font = pygame.font.Font(None, 100)
    window.blit(fon, (0, 0))
    pygame.display.flip()
    game_name = font.render('ПОБЕДА!', True, (255, 255, 255))
    game_name_rect = game_name.get_rect(center=(350, 50))
    window.blit(game_name, game_name_rect)
    if new >= old:
        txt_1 = f'Счёт - {new} Ходов'
        text_1 = font.render(txt_1, True, (255, 255, 255))
        text_rect_1 = text_1.get_rect(center=(300, 230))
        txt_2 = f'Рекорд - {old} Ходов'
        text_2 = font.render(txt_2, True, (255, 255, 255))
        text_rect_2 = text_2.get_rect(center=(350, 140))
        window.blit(text_1, text_rect_1)
        window.blit(text_2, text_rect_2)
        pygame.display.update()
        pygame.display.flip()
    else:
        txt = f'Счёт - {new} Ходов'
        text = font.render(txt, True, (255, 255, 255))
        text_rect = text.get_rect(center=(350, 230))
        window.blit(text, text_rect)
        text_record = font.render('НОВЫЙ РЕКОРД!', True, (255, 255, 255))
        window.blit(text_record, (40, 100))
    pygame.display.update()
    clock.tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    mouse_pos = pygame.mouse.get_pos()
                    button.check_active(mouse_pos)
                    button.event(event)
            if event.type == pygame.USEREVENT:
                if event.button.text == 'Выход':
                    pygame.quit()
                    sys.exit()


def main(): #Запускающая игру функция с обработчиком игровых событий
    moves = 0
    board = Board(W_game, H_game, IMAGE)
    start_screen(clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND, board)
    running = True
    game_events = Game_events(board)
    while running:
        check = [sp.ind for sp in sprites_group]
        game = [(sp.rect.x, sp.rect.y) for sp in sprites_group]
        check_1 = [sp.ind for sp in game_finish]
        game_1 = [(sp.rect.x, sp.rect.y) for sp in game_finish]
        if check == check_1 and game == game_1:
            window.blit(sprites[-1][0], (1252, 752))
            with open('records.txt', 'r') as f:
                old_moves = int(f.read())
            if moves < int(old_moves):
                with open('records.txt', 'w') as f:
                    f.write(str(moves))
            end_screen(old_moves, moves)
            running = False
        for event in pygame.event.get():
            for button in board.buttons:
                button.draw(window)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in board.buttons:
                    mouse_pos = pygame.mouse.get_pos()
                    button.check_active(mouse_pos)
                    button.event(event)
            if event.type == pygame.USEREVENT:
                if event.button.text == 'Настройки':
                    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
                    window.blit(fon, (0, 0))
                    pygame.display.flip()
                    settings = Settings()
                    settings.visible = True
                    settings.draw(window)
                    pygame.display.flip()
                elif event.button.text == 'Пауза':
                    board.buttons[0] = Buttons(1502, 350, 414, 175, 'Продолжить', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
                    board.render(window)
                    pygame.display.flip()
                elif event.button.text == 'Продолжить':
                    board.buttons[0] = Buttons(1502, 350, 414, 175, 'Пауза', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
                    board.render(window)
                    pygame.display.flip()
                elif event.button.text == 'Выход':
                    start_screen(clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND, board)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    result = game_events.move_up()
                    if result:
                        moves += 1
                elif event.key == pygame.K_DOWN:
                    result = game_events.move_down()
                    if result:
                        moves += 1
                elif event.key == pygame.K_LEFT:
                    result = game_events.move_left()
                    if result:
                        moves += 1
                elif event.key == pygame.K_RIGHT:
                    result = game_events.move_right()
                    if result:
                        moves += 1
                board.event(event)
        clock.tick(FPS)


#Создание спрайта для перемещения
empty_cell = Empty_sprite(EMPTY, 1500, 1000)
empty_sprite.add(empty_cell)


if __name__ == '__main__':
    main()
