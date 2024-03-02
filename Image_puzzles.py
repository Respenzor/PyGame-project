import pygame
import sys


GAME_NAME = 'Image Puzzles' #Название игры
BUTTON_IMAGE = 'knopka.png' #Изображение кнопки
BUTTON_ACTIVE_IMAGE = 'knopka_active.png' #Изображение кнопки при наведении на неё
BUTTON_SOUND = 'knopka_press.mp3' #Звук нажатия на кнопку

pygame.init()
W_game, H_game = 1920, 1000 #Размеры окна игры
pygame.display.set_caption(GAME_NAME)
W, H = 1920, 1080 #Размеры меню
FPS = 60 #Частота обновления экрана
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

def start_screen(clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND): #Функция отрисовки стартового окна
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
                        print('Нажата кнопка играть')
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

        pygame.display.update()
        clock.tick(FPS)

def main(): #Запускающая игру функция с обработчиком игровых событий
    start_screen(clock, FPS, W, H, GAME_NAME, BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)


if __name__ == '__main__':
    main()
