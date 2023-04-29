import pygame
from pygame import *
from random import randint
pygame.init()
 
mixer.init()
font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
 
FPS = 90
clock = time.Clock()
 
 
speed_r = 10
 
lost = 0
score = 0
healpoints = 3
 
window = display.set_mode((700, 500))
display.set_caption('Правое яйцо прадеда')
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
    def move_rocket(self):
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
 
    def update(self):
        self.rect.y += self.speed
        global lost, score, healpoints
        if self.rect.y > 500:
            self.speed = randint(1, 3)
            self.rect.x = randint(25, 650)
            self.rect.y = 0
            lost += 1
        
        sprites_list = sprite.groupcollide(ufos, bullets, True, True)
        for hz in sprites_list:
            score += 1
            ufo = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 2))
            ufos.add(ufo)

        sprites_list2 = sprite.spritecollide(rocket, ufos, True)
        for hzhz in sprites_list2:
            healpoints -= 1
            ufo = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 2))
            ufos.add(ufo)
        
        sprites_list3 = sprite.groupcollide(asteroids, bullets, False, True)

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 3)
        bullets.add(bullet)
        fire.play()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


background = GameSprite('galaxy.jpg', 0, 0, 700, 500, 0)
 
rocket = GameSprite('rocket.png', 350, 440, 50, 70, speed_r)
ufo = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 2))
ufo1 = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 4))
ufo2 = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 2))
ufo3 = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 4))
ufo4 = GameSprite('ufo.png', randint(25, 650), 25, 75, 45, randint(1, 3))
asteroid = GameSprite('asteroid.png', randint(25, 650), 25, 40, 40, 1)
asteroid1 = GameSprite('asteroid.png', randint(25, 650), 25, 40, 40, 1)
asteroid2= GameSprite('asteroid.png', randint(25, 650), 25, 40, 40, 1)
ufos = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
ufos.add(ufo, ufo1, ufo2, ufo3, ufo4)
asteroids.add(asteroid, asteroid1, asteroid2)
 
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
 
 
game = True
finish = False

 
win = font1.render('YOU WIN', 1, (110, 220, 30))
lose = font1.render('YOU LOSE', 1, (255, 255, 255))
 
 
spisok = []
while game:

    for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    rocket.fire()

    if finish == False:
        background.reset()

        text_lose = font2.render(
            'Пропущено: ' + str(lost), 1, (255,255,255)
        )

        text_score = font2.render(
            'Счёт: ' + str(score), 1, (255,255,255)
        )

        text_hp = hp = font2.render(
            'Жизни:' + str(healpoints), 1, (255, 255, 255)
        )
    
        window.blit(text_lose, (10, 10))
        window.blit(text_score, (10, 50))
        window.blit(text_hp, (10, 90))
    
        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
        rocket.reset()
        asteroids.draw(window)
        asteroids.update()
    
    
        keys = key.get_pressed()
        rocket.move_rocket()
    
        

        if healpoints <= 0:
            finish = True
    else:
        background.reset()
        window.blit(lose, (225, 220))

    clock.tick(FPS)
    display.update()