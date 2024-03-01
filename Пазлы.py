import pygame
import sys

pygame.init()
W, H = 800, 700
FPS = 60
size = W, H
screen = pygame.display.set_mode(size)
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
black_color = (0, 0, 0)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

GAME_NAME = 'Magick Puzzles'
BUTTON_IMAGE = 'knopka.png'
BUTTON_ACTIVE_IMAGE = 'knopka_active.png'
BUTTON_SOUND = 'knopka_press.mp3'


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
        self.visible = True

    def draw(self, window):
        if self.visible:
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


class Settings:
    def __init__(self):
        self.visible = False

    def draw(self, window):
        global event
        if self.visible:
            fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
            window.blit(fon, (0, 0))
            pygame.display.flip()

            sound_button = Buttons(250, 235, 300, 100, 'Звуки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            game_settings_button = Buttons(250, 355, 300, 100, 'Игра', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            back_button = Buttons(250, 475, 300, 100, 'Назад', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            absolute_back = Buttons(250, 475, 300, 100, 'Назад', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
            buttons = [sound_button, game_settings_button, back_button, absolute_back]

            def hide_buttons(buttons):
                for button in buttons:
                    button.visible = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        absolute_back.event(event)



            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in buttons:
                            button.event(event)

                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_active(mouse_pos)

                for button in buttons:
                    button.draw(window)
                pygame.display.update()
                clock.tick(FPS)

                if event.type == pygame.USEREVENT:
                    if event.button == sound_button:
                        sound_button = Buttons(250, 235, 300, 100, 'Звуки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE)
                        game_settings_button = Buttons(250, 355, 300, 100, 'Игра', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE)
                        back_button = Buttons(250, 475, 300, 100, 'Назад', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE)
                        buttons = [sound_button, game_settings_button, back_button]
                        hide_buttons(buttons)

                        fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
                        window.blit(fon, (0, 0))




def start_screen(absolute_back):
    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
    font = pygame.font.Font(None, 125)
    window.blit(fon, (0, 0))
    pygame.display.flip()

    game_name = font.render(GAME_NAME, True, (255, 255, 255))
    game_name_rect = game_name.get_rect(center=(W // 2, 110))
    window.blit(game_name, game_name_rect)
    pygame.display.flip()

    start_button = Buttons(250, 235, 300, 100, 'Играть', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    options_button = Buttons(250, 355, 300, 100, 'Настройки', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    quit_button = Buttons(250, 475, 300, 100, 'Выход', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)
    buttons = [start_button, options_button, quit_button]

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
                    print('0 ')
                elif event.button == options_button:
                    hide_buttons(buttons, absolute_back)
                    fon = pygame.transform.scale(pygame.image.load('fon_menu.jpg'), (W, H))
                    window.blit(fon, (0, 0))
                    pygame.display.flip()

                    settings = Settings()
                    settings.visible = True
                    settings.draw(window)

                elif event.button == quit_button:
                    pygame.quit()
                    sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_active(mouse_pos)

        for button in buttons:
            button.draw(window)
        pygame.display.update()
        clock.tick(FPS)


def hide_buttons(buttons, absolute_back):
    buttons.append(absolute_back)
    for button in buttons:
        if button != absolute_back:
            button.visible = False
        else:
            button.visible = True


def show_buttons(buttons):
    for button in buttons:
        button.visible = True


if __name__ == '__main__':
    absolute_back = Buttons(250, 475, 300, 100, 'Назад', BUTTON_IMAGE, BUTTON_ACTIVE_IMAGE, BUTTON_SOUND)

    start_screen(absolute_back)
