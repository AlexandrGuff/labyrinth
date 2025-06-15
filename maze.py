#создай игру "Лабиринт"!
import pygame
pygame.init()
from pygame import mixer
from pygame import font
mixer.init()



W, H = 700, 500
FPS = 160
VIOLET = 123, 104, 238
font = font.Font(None, 70)

window = pygame.display.set_mode((W, H))
pygame.display.set_caption('Maze')
background_image = pygame.transform.scale(pygame.image.load('background.jpg'), (W, H)) 

clock = pygame.time.Clock()

pygame.mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()



class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, weight, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), (weight, height))
        self.speed = speed
        self.rect = self.image.get_rect() #hitbox
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < W:
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x -= self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x += self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < H:
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y -= self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y += self.speed
            

class Enemy(GameSprite):
    direction = 'left'
    def update(self, x1, x2):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x <= x1:
            self.direction = 'right'
        if self.rect.right == x2:
            self.direction = 'left'

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, self.rect)

        


enemy = Enemy('cyborg.png', 500, 300, 50, 50, 2)
player = Player('hero.png', 100, 150, 50, 50, 5)
gold = GameSprite('treasure.png', 600, 400, 50, 50, 1)


walls = pygame.sprite.Group()
walls.add(
    Wall(170, 20, 15, 325, VIOLET), 
    Wall(170, 20, 450, 15, VIOLET), 
    Wall(170, 450, 300, 15, VIOLET)
)


win = font.render('YOU WIN', True, (255, 215, 0))
lose = font.render('YOU LOSE', True, (255, 215, 0))
 
finish = False
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False



    
    if pygame.sprite.collide_rect(player, gold):
        window.blit(win, (200, 200))
        money = mixer.Sound('money.ogg')
        money.play()
        finish = True

    if pygame.sprite.collide_rect(player, enemy):
        window.blit(lose, (200, 200))
        kick = mixer.Sound('kick.ogg')
        kick.play()
        finish = True

    if not finish:
        window.blit(background_image, (0, 0))
        player.update()
        enemy.update(450, 650)
        player.reset()
        enemy.reset()
        gold.reset()
        walls.draw(window)

    

    pygame.display.update()
    clock.tick(FPS)

