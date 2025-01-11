from pygame import*
from random import randint

mixer.init()
mixer.music.load('music.ogg')
mixer_music.play()
fire_sound = mixer.Sound('shutt.ogg')

font.init()
font2 = font.Font(None, 36)

img_back = "kosmo.png"
img_hero = "rocket.png"
img_enemy = "baxa.jpg"

clock = time.Clock()
FPS = 60

score = 0 
lost = 0


class GameSprite(sprite.Sprite):    
    def __init__ (
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_speed
    ):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
 
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        pass

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0 
            lost = lost + 1

 
# створюємо віконце
win_width = 700
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
    80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)
 
# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
 
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
 
while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
 
    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 250))
        window.blit(text, (10, 20))

        text_lose = font2.render(f"Пропущено: {lost}", 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
         
 
        # рухи спрайтів
        ship.update()
        monsters.update()
 
        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
 
    display.update()
    clock.tick(FPS)



