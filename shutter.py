from pygame import*

mixer.init()
mixer.music.load('music.ogg')
mixer_music.play()
fire_sound = mixer.Sound('shutt.ogg')


img_back = "kosmo.png"
img_hero = "shu.jpg"

clock = time.Clock()
FPS = 60


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
 
 
# створюємо віконце
win_width = 700
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
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
 
        # рухи спрайтів
        ship.update()
 
        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
 
    display.update()
    clock.tick(FPS)



