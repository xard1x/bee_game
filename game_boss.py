from pygame import *
from random import randint
from pygame import sprite
from time import sleep

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
                self.rect.x = randint(80, 1000 - 80)
                self.rect.y = -50
    class Enemy_Horiz(GameSprite):
        def update(self): # метод для автоматического передвижения
            self.rect.x += self.speed  # двигаем врага вниз
            if self.rect.x > 1000:
                self.rect.y = randint(80, 700 - 80)
                self.rect.x = -50
    class Boss(sprite.Sprite):
        def __init__(self, image_file, x, y, speed):
            super().__init__()
            self.image = transform.scale(image.load(image_file), (100, 100))
            self.speed = speed
            self.rect = self.image.get_rect()  # прозрачная подложка спрайта - физическая модель
            self.rect.x = x
            self.rect.y = y
            self.vector = Vector2(1 , 1).normalize()
        def update(self):
            if self.rect.x <= 850 and self.rect.y >= 100:   
                self.rect.x += self.speed *  self.vector.x
            if self.rect.x >= 850 and self.rect.y >= 100 and  self.rect.y < 450:
                self.rect.y += self.speed * self.vector.y
            if self.rect.y >= 450 and self.rect.x <= 850 and self.rect.x >= 850:
                self.rect.x += -self.vector.x * self.speed
            if self.rect.x <= 850 and self.rect.y >= 500:
                self.rect.y += self.vector.y * self.speed

        def reset(self):
            window_game.blit(self.image, (self.rect.x, self.rect.y))
            
    print(count)
    window_game = display.set_mode((1000, 700))
    display.set_caption('Босс')
    background = transform.scale(image.load('field.jpg'), (1000, 700))

    clock = time.Clock()
    FPS = 60
    game = True
    finish = False

    player = Player("bee_player.png", 500, 350, 4)
    boss = Boss('boss.png', 150, 100, 7)
    monsters = sprite.Group()
    monsters1 = sprite.Group()

    font2 = font.SysFont("Arial", 80)
    lose_font = font2.render("Ты проиграл!", True, (255, 0, 0))

    mixer.init()
    #mixer.music.load('music.mp3')
    #mixer_music.play(loops= -1)
    kick = mixer.Sound('defeat.mp3')
    #take = mixer.Sound('take.mp3')
    #win = mixer.Sound('win.mp3')

    for i in range(count):
        monster = Enemy_Vert('bug.png', randint(0, 1000 - 80), -40, randint(1, 4),)
        monsters.add(monster)
    for i in range(count):
        monster1 = Enemy_Horiz('bug.png', 10, randint(80, 700 - 80), randint(1, 4),)
        monsters1.add(monster1)

    while game:  # игровой цикл
        if finish != True:
            window_game.blit(background, (0, 0))
            boss.update()
            boss.reset()
            monsters.update()
            monsters1.update()
            monsters.draw(window_game)
            monsters1.draw(window_game)
            player.update()
            player.reset()
            if sprite.spritecollideany(player, monsters1) or sprite.spritecollideany(player, monsters):
                finish = True
                window_game.blit(lose_font, (220, 220))
                kick.play()
                player.rect.x = randint(20, 980)
                player.rect.y = randint(20, 680)
        else:
            finish = False
            time.delay(3000)
                
        for e in event.get():
            if e.type == QUIT:
                game = False
        clock.tick(FPS)
        display.update()
