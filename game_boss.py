from pygame import *
from random import randint
def boss(count):
    class GameSprite(sprite.Sprite): #класс спрайта
        def __init__(self, image_file, x, y, speed):
            super().__init__()
            self.image = transform.scale(image.load(image_file), (50, 50))  # создание внешнего вида спрайта - картинки
            self.speed = speed
            self.rect = self.image.get_rect()  # прозрачная подложка спрайта - физическая модель
            self.rect.x = x
            self.rect.y = y
        def reset(self):
            window_game.blit(self.image, (self.rect.x, self.rect.y))
    class Player(GameSprite): #класс игрока
        def update(self): # метод для управления спрайтом
            keys = key.get_pressed()  # набор всех нажатых клавиш
            if keys[K_w] and self.rect.y > - 10:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < 700 - 50:
                self.rect.y += self.speed
            if keys[K_a] and self.rect.x > -10:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.x < 1000 - 50:
                self.rect.x += self.speed
    class Enemy_Vert(GameSprite):
        def update(self): # метод для автоматического передвижения
            self.rect.y += self.speed  # двигаем врага вниз
            if self.rect.y > 700:
                # устанавливаем случайную координату по X
                self.rect.x = randint(80, 1000 - 80)
                # устанавливаем координату по Y (немного выше верхней границы)
                self.rect.y = -50
    class Enemy_Horiz(GameSprite):
        def update(self): # метод для автоматического передвижения
            self.rect.y += self.speed  # двигаем врага вниз
            if self.rect.y > 700:
                # устанавливаем случайную координату по X
                self.rect.x = randint(80, 1000 - 80)
                # устанавливаем координату по Y (немного выше верхней границы)
                self.rect.y = -50
    print(count)
    window_game = display.set_mode((1000, 700))
    display.set_caption('Босс')
    background = transform.scale(image.load('field.jpg'), (1000, 700))

    clock = time.Clock()
    FPS = 60
    game = True
    finish = False

    player = Player("bee_player.png", 5, 700 - 80, 4)


    while game:  # игровой цикл
        if finish != True:
            window_game.blit(background, (0, 0))
            player.update()
            player.reset()
        for e in event.get():
            if e.type == QUIT:
                game = False
        clock.tick(FPS)
        display.update()
