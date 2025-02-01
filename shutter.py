from pygame import*
from random import randint
import time as pytime

mixer.init()
mixer.music.load("assets\\sounds\\music.ogg")
mixer_music.play()
fire_sound = mixer.Sound("assets\\sounds\\shutt.ogg")


font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


img_back = "assets\\pictures\\kosmo.png"
img_hero = "assets\\pictures\\rocket.png"
img_enemy = "assets\\pictures\\nlo.png"
img_bullet = "assets\\pictures\\nagets.png"

clock = time.Clock()
FPS = 60


score = 0 
goal = 50
lost = 0
max_lost = 3
life = 3
bullet_count = 10
reload_start_time = None


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

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

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
        bullet = Bullet (
            img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15  
        )
        bullets.add(bullet)

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
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

bullets = sprite.Group()

# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
 
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
 
while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and bullet_count > 0 and reload_start_time is None:
                bullet_count -= 1
                fire_sound.play()
                ship.fire()
 
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
        bullets.update()
        bullets.draw(window)
 
        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        if bullet_count == 0 and reload_start_time is None:
            reload_start_time = pytime.time()

        if reload_start_time:
            if pytime.time() - reload_start_time > 3:
                bullet_count = 10
                reload_start_time = None
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score = score + 1 
            monster = Enemy(
                img_enemy,
                randint(80, win_width - 80), -40, 80, 50, randint(1, 5)
            )
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, True):
            life -= 1
            monster = Enemy(
                img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)
            )
            monsters.add(monster)
        
        text_life = font1.render(str(life), 1, (255, 0, 0))
        window.blit(text_life, (650, 10))

        if life == 0 or lost >= max_lost:
            finish = True
            mixer.music.stop()
            window.blit(lose, (200, 200)) 

        if score >= goal:
            finish = True
            mixer.music.stop()
            window.blit(win, (200, 200))
                        
                

            
    display.update()
    clock.tick(FPS)



