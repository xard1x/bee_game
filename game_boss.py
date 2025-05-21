from pygame import *
from random import randint
from pygame import sprite
import os
import sys

def boss(count):
    class GameSprite(sprite.Sprite): #класс спрайта
        def __init__(self, image_file, x, y, speed):
            super().__init__()
            self.image = transform.scale(image.load(image_file), (50, 50))  # создание внешнего вида спрайта - картинки
            self.speed = speed
            self.rect = self.image.get_rect()  # прозрачная подложка спрайта - физическая модель
            self.rect.x = x
            self.rect.y = y
            self.vector = Vector2(1 , 1).normalize()
        def reset(self):
            window_game.blit(self.image, (self.rect.x, self.rect.y))
    class Player(GameSprite): #класс игрока
        def __init__(self, player_x, player_y, player_image, player_speed):
            super().__init__(player_x, player_y, player_image, player_speed)
            self.reload_time = 0.9
            self.cur_reload_time = 0
            self.is_reloading = False
        def update(self): # метод для управления спрайтом
            global direction
            keys = key.get_pressed()  # набор всех нажатых клавиш
            if keys[K_w] and self.rect.y > - 10:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < 700 - 50:
                self.rect.y += self.speed
            if keys[K_a] and self.rect.x > -10:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.x < 1000 - 50:
                self.rect.x += self.speed
            if keys[K_LEFT]:
                direction = 'left'
            if keys[K_RIGHT]:
                direction = 'right'
            if keys[K_UP]:
                direction = 'up'
            if keys[K_DOWN]:
                direction = 'down'

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
        def __init__(self, image_file, x, y, speed, hp):
            super().__init__()
            self.image = transform.scale(image.load(image_file), (100, 100))
            self.speed = speed
            self.rect = self.image.get_rect()  # прозрачная подложка спрайта - физическая модель
            self.rect.x = x
            self.rect.y = y
            self.vector = Vector2(1 , 1).normalize()
            self.hp = hp
        def update(self):
            if self.rect.y == 100 and self.rect.x >= 150 or self.rect.x >= 140 and self.rect.y <= 100 :
                self.rect.x += self.speed *  self.vector.x
            if self.rect.y >= 100 and self.rect.y <= 500 and  self.rect.x >= 850:
                self.rect.y += self.speed * self.vector.y
            if self.rect.y >= 505 and self.rect.x <= 850:
                self.rect.x += -self.vector.x * self.speed
            if self.rect.x <= 850 and self.rect.x <= 140 and self.rect.y <= 505:
                self.rect.y += -self.vector.y * self.speed
        def reset(self):
            window_game.blit(self.image, (self.rect.x, self.rect.y))

    class Bullet(sprite.Sprite):
        def __init__(self, image_file, x, y, speed, direction):
            super().__init__()
            self.image = transform.scale(image.load(image_file), (30, 30))
            self.speed = speed
            self.rect = self.image.get_rect() 
            self.rect.x = x
            self.rect.y = y
            self.direction = direction
        def update(self):
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            if not 0 <= self.rect.x <= 1000 or not 0 <= self.rect.y <= 700:
                self.kill()
    
    class Wall(sprite.Sprite):  # класс для спрайтов-стен
        def __init__(self, r, g, b, x, y, width, height):
            super().__init__()
            self.r = r
            self.g = g
            self.b = b
            self.width = width
            self.height = height
            self.image = Surface((self.width, self.height))
            self.image.fill((r, g, b))  # заливаем цветом
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        def draw_wall(self): # отображает картинку в координатах физической модели
            window_game.blit(self.image, (self.rect.x, self.rect.y))

    bullets = sprite.Group()
    all_sprites = sprite.Group()
     

    window_game = display.set_mode((1000, 700))
    display.set_caption('Босс')
    background = transform.scale(image.load('field.jpg'), (1000, 700))

    clock = time.Clock()
    FPS = 60
    game = True
    finish = False

    flower = GameSprite("flower.png", randint(20, 980), randint(20, 680), 0)
    player = Player("bee_player.png", 500, 350, 4)
    boss = Boss('boss.png', 150, 100, 7, 3 * count)

    green_len = 10 * boss.hp
    wall_boss_back = Wall(105, 105, 105, 350 , 10, 300 , 35)
    wall_boss = Wall(0, 255, 0, 360 , 15, green_len , 25)

    monsters = sprite.Group()
    monsters1 = sprite.Group()
    all_sprites.add(flower, player, boss)

    font1 = font.SysFont("Arial", 50)
    font2 = font.SysFont("Arial", 80)
    lose_font = font2.render("Ты проиграл!", True, (255, 0, 0))

    mixer.init()
    mixer.music.load('music.mp3')
    mixer_music.play(loops= -1)
    kick = mixer.Sound('defeat.mp3')
    take = mixer.Sound('take.mp3')
    win = mixer.Sound('win.mp3')

    for i in range(count):
        monster = Enemy_Vert('bug.png', randint(0, 1000 - 80), -40, randint(1, 4),)
        monsters.add(monster)
        all_sprites.add(monster)
    for i in range(count):
        monster1 = Enemy_Horiz('bug.png', 10, randint(80, 700 - 80), randint(1, 4),)
        monsters1.add(monster1)
        all_sprites.add(monster1)

    ammo = 3

    while game:  # игровой цикл
        if finish != True:
            window_game.blit(background, (0, 0))
            wall_boss_back.draw_wall()
            wall_boss.draw_wall()
            ammo_font = font1.render("Патроны:" + str(ammo), True, (255, 255, 255))
            window_game.blit(ammo_font, (10, 10))
            all_sprites.update()
            bullets.update()
            boss.reset()
            bullets.draw(window_game)
            monsters.draw(window_game)
            monsters1.draw(window_game)
            player.reset()
            flower.reset() 
            if green_len > 290:
                green_len = 280
                wall_boss = Wall(0, 255, 0, 360 , 15, green_len , 25)   
            if sprite.collide_rect(player, flower):
                ammo += 3
                flower.rect.x = randint(20, 980)
                flower.rect.y = randint(20, 680)
                take.play()
            if sprite.spritecollideany(player, monsters1) or sprite.spritecollideany(player, monsters) or sprite.collide_rect(player, boss):
                finish = True
                window_game.blit(lose_font, (220, 220))
                boss.hp += 3
                green_len = 10 * boss.hp
                wall_boss = Wall(0, 255, 0, 360 , 15, green_len , 25)
                kick.play()
                player.rect.x = randint(20, 980)
                player.rect.y = randint(20, 680)
            if sprite.spritecollideany(boss, bullets):
                bullet.kill()
                boss.hp -= 1
                green_len = 10 * boss.hp
                wall_boss = Wall(0, 255, 0, 360 , 15, green_len , 25)
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                boss.hp += 1
                green_len = 10 * boss.hp
                wall_boss = Wall(0, 255, 0, 360 , 15, green_len , 25)
                monster = Enemy_Vert('bug.png', randint(0, 1000 - 80), -40, randint(1, 4),)
                monsters.add(monster)
                all_sprites.add(monster)
            collides1 = sprite.groupcollide(monsters1, bullets, True, True)
            for c in collides1:
                boss.hp += 1
                monster1 = Enemy_Horiz('bug.png', 10, randint(80, 700 - 80), randint(1, 4),)
                monsters1.add(monster1)
                all_sprites.add(monster1)
            if boss.hp <= 0:
                win.play()
                time.delay(1000)
                os.execv(sys.executable, ['python'] + sys.argv)
        else:
            finish = False
            time.delay(3000)
                
        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if ammo > 0:   
                    if e.key == K_LEFT:
                        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 15, (-1, 0))
                        bullets.add(bullet)
                        ammo -= 1
                    if e.key == K_RIGHT:
                        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 15, (1, 0))
                        bullets.add(bullet)
                        ammo -= 1
                    if e.key == K_UP:
                        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 15, (0, -1))
                        bullets.add(bullet)
                        ammo -= 1
                    if e.key == K_DOWN:
                        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 15, (0, 1))
                        bullets.add(bullet)
                        ammo -= 1

        clock.tick(FPS)
        display.update()
