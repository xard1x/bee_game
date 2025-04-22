from PyQt5.QtCore import Qt
from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pygame import *
from time import sleep

def msg_box():    
    msg = QMessageBox() #всплывающее окно
    msg.setIcon(QMessageBox.Information) 
    msg.setWindowTitle("Цель игры")
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok) 
    msg.exec_() 

def game(): # функция игры
    global text
    text = 'Цель: собрать 10 цветков не косаясь жуков и стен'
    msg_box()
    global num_wall  #переменные для настройки
    num_wall = int(line_edit.text())
    global num_enemy
    num_enemy = int(line_edit1.text())
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
            
    class Enemy(GameSprite):# класс врага
        direction = "left"  # начальное направление
        def update(self): # метод для автоматического передвижения
            global lost  # используем глобальную переменную
            self.rect.y += self.speed  # двигаем врага вниз
            if self.rect.y > 700:
                # устанавливаем случайную координату по X
                self.rect.x = randint(80, 1000 - 80)
                # устанавливаем координату по Y (немного выше верхней границы)
                self.rect.y = -50
                # к количеству пропущенных прибавляем 1
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

    flower_count = 0 #кол-во собранных цветов
    window.close()
    window_game = display.set_mode((1000, 700))
    display.set_caption('Игра')

    background = transform.scale(image.load('field.jpg'), (1000, 700))
    flower = GameSprite("flower.png", randint(20, 980), randint(20, 680), 0)
    player = Player("bee_player.png", 5, 700 - 80, 4)
    monsters = sprite.Group()
    for i in range(num_enemy):
        monster = Enemy('bug.png', randint(0, 1000 - 80), -40, randint(1, 4),)
        monsters.add(monster)
    walls_list = []
    for i in range(num_wall):
        wall = Wall(30 , 89, 69, randint(100, 880), randint(100, 200), 35, 300)
        walls_list.append(wall)
        walls = sprite.Group()
        walls.add(walls_list)
    
    clock = time.Clock()
    FPS = 60
    game = True
    finish = False

    mixer.init()
    mixer.music.load('music.mp3')
    mixer_music.play(loops= -1)
    kick = mixer.Sound('defeat.mp3')
    take = mixer.Sound('take.mp3')
    win = mixer.Sound('win.mp3')

    font.init()
    font1 = font.SysFont("Arial", 50)
    font2 = font.SysFont("Arial", 80)
    win_font = font2.render("Ты выиграл!", True, (255, 255, 255))
    lose_font = font2.render("Ты проиграл!", True, (255, 0, 0))
    boss_text = font2.render("", True, (255, 255, 255))

    while game: #игровой цикл
        if finish != True:            
            player.update()
            monsters.update()
            window_game.blit(background, (0, 0))
            flower_font = font1.render("Счёт:" + str(flower_count), True, (255, 255, 255))
            window_game.blit(flower_font, (10, 20))
            monsters.draw(window_game)
            player.reset()
            flower.reset()
            for i in range(int(num_wall)): # num_wall должен быть строкой, конвертируемой в int
                walls_list[i].draw_wall()
            if flower_count == 10:
                finish = True
                window_game.blit(win_font, (200, 200))
                win.play()
                
            if sprite.collide_rect(player, flower):
                flower.rect.x = randint(20, 980)
                flower.rect.y = randint(20, 680)
                take.play()
                flower_count += 1
            if sprite.spritecollide(player, walls_list, False) or sprite.spritecollideany(player, monsters):
                finish = True
                window_game.blit(lose_font, (220, 220))
                kick.play()
                player.rect.x = randint(20, 980)
                player.rect.y = randint(20, 680)
            if sprite.spritecollide(flower, walls_list, False):
                flower.rect.x = randint(20, 980)
                flower.rect.y = randint(20, 680)
        else:
            finish = False
            flower_count = 0
            flower.rect.x = randint(20, 980)
            flower.rect.y = randint(20, 680)
            time.delay(3000)
        for e in event.get():
            if e.type == QUIT:
                game = False
        clock.tick(FPS)
        display.update()

app = QApplication([]) # создание окна
window = QWidget()

pal = QPalette()
pal.setColor(QPalette.Window, QColor(0, 0, 0))
window.setPalette(pal)
window.setAutoFillBackground(True)
 
window.setWindowTitle('Настройки')  #название и размер окна
window.setMinimumSize(400, 400)
window.setMaximumSize(400, 400)

main_layout = QVBoxLayout() #создание основного лайаута

horiz_layout_1 = QHBoxLayout() # надпись настройки
label_setting = QLabel('<h1 style="color: rgb(255, 255, 255);">Настройки</h1>', alignment=Qt.AlignCenter)
label_setting.setFont(QFont('Arial', 20)) 
horiz_layout_1.addWidget(label_setting,alignment = Qt.AlignCenter)

horiz_layout_2 = QHBoxLayout() #надпись с инфой
label_info = QLabel('<h4 style="color: rgb(255, 255, 255);">Напиши кол-во ограждений и врагов:</h4>', alignment=Qt.AlignCenter)
label_info.setFont(QFont('Arial', 13)) 
horiz_layout_2.addWidget(label_info,alignment = Qt.AlignCenter)

horiz_layout_3 = QHBoxLayout() #кнопки
label_info1 = QLabel('<h4 style="color: rgb(255, 255, 255);">Кол-во ограждений:</h4>', alignment=Qt.AlignCenter)
label_info1.setFont(QFont('Arial', 13))
line_edit = QLineEdit()
line_edit.setValidator(QIntValidator(1, 9))
horiz_layout_3.addWidget(label_info1,alignment = Qt.AlignCenter)
horiz_layout_3.addWidget(line_edit,alignment = Qt.AlignCenter)

horiz_layout_4 = QHBoxLayout() #кнопки
label_info2 = QLabel('<h4 style="color: rgb(255, 255, 255);">Кол-во врагов:</h4>', alignment=Qt.AlignCenter)
label_info2.setFont(QFont('Arial', 13))
line_edit1 = QLineEdit()
line_edit1.setValidator(QIntValidator(1, 9))
horiz_layout_4.addWidget(label_info2,alignment = Qt.AlignCenter)
horiz_layout_4.addWidget(line_edit1,alignment = Qt.AlignCenter)

horiz_layout_5 = QHBoxLayout() #кнопка начать игру
button_play = QPushButton('Начать игру')
button_play.setFont(QFont('Arial', 20))
horiz_layout_5.addWidget(button_play,alignment = Qt.AlignCenter)

button_play.clicked.connect(game)
main_layout.addLayout(horiz_layout_1)
main_layout.addLayout(horiz_layout_2)
main_layout.addLayout(horiz_layout_3)
main_layout.addLayout(horiz_layout_4)
main_layout.addLayout(horiz_layout_5)
window.setLayout(main_layout)
window.show()
app.exec()
