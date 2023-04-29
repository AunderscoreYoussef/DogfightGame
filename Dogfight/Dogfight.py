import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()
pygame.mixer.init()
import time
from pygame import mixer


#limiting screen frames
clock = pygame.time.Clock()
fps = 60


#screen adjustments
screenWidth = 700
screenHeight = 700
screen = pygame.display.set_mode((screenWidth, screenHeight))

font = pygame.font.Font("data/font/VT323-Regular.ttf", 40)



#hp colors
red = (255, 0, 0)
green = (0, 255, 0)

beige = (225, 198, 153)


bg = pygame.image.load("data/imgs/bg.jpg").convert_alpha()
bgMusic = mixer.music.load("data/music/background.mp3")
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)


hitSound = mixer.Sound("data/music/hit.mp3")
boomSound = mixer.Sound("data/music/boom.mp3")
shootSound = mixer.Sound("data/music/shot.mp3")

hitSound.set_volume(0.03)
boomSound.set_volume(0.04)
shootSound.set_volume(0.03)



pygame.display.set_caption("Dogfight")

#drawing and scaling background image to fit "screenWidth" and "screenHeight"
def drawBg():
    screen.blit(bg, (0, 0))


#Making airplane class
class Airplane(pygame.sprite.Sprite):
    def __init__(self, name, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load(f"data/imgs/{name}/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.maxHealth = health
        self.remainingHealth = health
        self.lastShot = pygame.time.get_ticks()

    def update(self):
        #movement speed
        speed = 3

        #cooldown for shot
        cooldown = 500
        
        #keypresses
        if self.name == "p1":
            key = pygame.key.get_pressed()
            if key[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= speed
                key = pygame.key.get_pressed()
            if key[pygame.K_d] and self.rect.right < screenWidth:
                self.rect.x += speed

        if self.name == "p2":
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
                key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT] and self.rect.right < screenWidth:
                self.rect.x += speed

        


        #time between bullets
        currentTime = pygame.time.get_ticks()


        #shoot
        if self.name == "p1":
            if key[pygame.K_SPACE] and currentTime - self.lastShot > cooldown:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bulletGroup.add(bullet)
                self.lastShot = currentTime
                shootSound.play()

        if self.name == "p2":
            if key[pygame.K_RETURN] and currentTime - self.lastShot > cooldown:
                bullet = Bullet2(self.rect.centerx, self.rect.bottom)
                bulletGroup.add(bullet)
                self.lastShot = currentTime
                shootSound.play()

        #update mask
        self.mask = pygame.mask.from_surface(self.image)
        outlineMask =  pygame.mask.from_surface(self.image).outline()

        #health bar
        if self.name == "p1":
            
            if self.remainingHealth > 0:
                pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 0), self.rect.width, 2))
                pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 0), int(self.rect.width * (self.remainingHealth / self.maxHealth)), 2))
            elif self.remainingHealth <= 0:
                pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 20), self.rect.width, 2))
                pygame.draw.rect(screen, beige, pygame.Rect(0, 0, 700, 60))
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                explosionGroup.add(explosion)
                p2.image = self.image = pygame.image.load(f"data/imgs/end/disappear.png")
                explosion.kill()
                self.kill()
                p2.kill()
                txt = font.render(f" Player 2 won!", 0, (0, 0, 0))
                screen.blit(txt, (1, 20, 700, 60))
                

        if self.name == "p2":
            if self.remainingHealth > 0:
                pygame.draw.rect(screen, red, (self.rect.x, (self.rect.top - 0), self.rect.width, 2))
                pygame.draw.rect(screen, green, (self.rect.x, (self.rect.top + 0), int(self.rect.width * (self.remainingHealth / self.maxHealth)), 2))
                if p1.remainingHealth <= 0:
                    pygame.draw.rect(screen, beige, (self.rect.x, (self.rect.top - 0), self.rect.width, 2))
            elif self.remainingHealth <= 0 and p1.remainingHealth > 0:
                pygame.draw.rect(screen, beige, pygame.Rect(0, 0, 700, 60))
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                p1.image = self.image = pygame.image.load(f"data/imgs/end/disappear.png")
                explosionGroup.add(explosion)
                explosion.kill()
                self.kill()
                p2.kill()
                
                txt = font.render(f" Player 1 won!", 0, (0, 0, 0))
                screen.blit(txt, (1, 20, 700, 60))
                
        
            


#create bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"data/imgs/bullet/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.name = p1.name
        
        

    def update(self):
        if self.name == p1.name:
            self.rect.y -= 5
            if self.rect.bottom < 0:
                self.kill()
        if pygame.sprite.spritecollide(self, airplaneGroup, False, pygame.sprite.collide_mask):
            self.kill()
            p2.remainingHealth -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion)
            hitSound.play()
            if p2.remainingHealth <= 0:
                boomSound.play()
            
       

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"data/imgs/bullet/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.name = p2.name

    def update(self):
        if self.name == p2.name:
            self.rect.y += 5
            if self.rect.y > 760:
                self.kill()
        if pygame.sprite.spritecollide(self, airplaneGroup, False, pygame.sprite.collide_mask):
            self.kill()
            p1.remainingHealth -= 1   
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion) 
            hitSound.play() 
            if p1.remainingHealth <= 0:
                boomSound.play()

        
#explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 4):
            img = pygame.image.load(f"data/imgs/exp/{i}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (60, 60))

            self.images.append(img)
            
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosionSpeed = 3
        self.counter += 1
        if self.counter >= explosionSpeed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosionSpeed:
            self.kill()
            
            



#sprite groups
airplaneGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group() 
explosionGroup = pygame.sprite.Group()

#creating player
p1 = Airplane("p1", int(screenWidth / 2), screenHeight - 50, 3)
airplaneGroup.add(p1)

p2 = Airplane("p2", int(screenWidth / 2), screenHeight - 650, 3)
airplaneGroup.add(p2)


run = True
while run:

    clock.tick(fps)

    #calling function to show us the background
    drawBg()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #in case of event of exiting the game - run turns to False
            #which closes the window

    #updateAirplane
    p1.update()
    p2.update()


    #drawing sprite groups
    airplaneGroup.draw(screen)
    bulletGroup.draw(screen)
    explosionGroup.draw(screen)

    #updating sprite groups
    bulletGroup.update()
    explosionGroup.update()

    #constantly updating display
    pygame.display.update()

pygame.quit()

