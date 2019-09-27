
import random
import pygame
from pygame.locals import *

Screen_Width =400
Screen_Height=600
margin =5

wallTop = margin
wallLeft = margin
wallRight =Screen_Width - margin
wallBottom =Screen_Height - margin

#load images
playerImg =pygame.image.load('images/twinbee.png')
backgroundImg=pygame.image.load('images/background.png')
bulletImg= pygame.image.load('images/bullet.png')

pygame.init()

screen=pygame.display.set_mode((Screen_Width,Screen_Height))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.img = pygame.image.load('images/twinbee.png').conver()
        self.surf= pygame.Surface((20,50))
        self.surf.fill((255,244,233))
        self.posX= Screen_Width/2
        self.posY= wallBottom
        self.rect = self.surf.get_rect(center=(self.posX,self.posY))
    
    def update(self):
        if self.rect.left<wallLeft :
            self.rect.left=wallLeft
        if self.rect.right > wallRight:
            self.rect.right = wallRight
        if self.rect.top < wallTop:
            self.rect.top = wallTop
        if self.rect.bottom >= wallBottom:
            self.rect.bottom = wallBottom
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf =pygame.Surface((5,5))
        self.surf.fill((100,255,255))
        self.rect=self.surf.get_rect(center=(player.posX,player.rect.y-30))
       # self.speed=5
    def update(self):
        self.rect.y -=3

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((10,20))
        self.surf.fill((233,233,211))
        self.rect=self.surf.get_rect
    
#list of every sprite.
all_sprites_list = pygame.sprite.Group()
#list of each enemies
enemy_list = pygame.sprite.Group()
#list of each bullet
bullet_list= pygame.sprite.Group()

#--Create the sprites
for i in range(50):
    enemy=Enemy()
    enemy.rect.x= random.randrange(Screen_Width)
    enemy.rect.y= random.randrange(Screen_Height)

    enemy_list.add(enemy)
    all_sprites_list.add(enemy)

player=Player()
all_sprites_list.add(player)

running= True
clock=pygame.time.Clock()
score=0

while running:
    for event in pygame.event.get():
        if event.type ==QUIT:
            running =False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running=False
            if event.key == pygame.K_UP:
                player.rect.y -=1
            if event.key == pygame.K_DOWN:
                player.rect.y +=1
            if event.key == pygame.K_LEFT:
                player.rect.x -=1
            if event.key == pygame.K_RIGHT:
                player.rect.x +=1  
            if event.key == pygame.K_SPACE:  
                bullet=Bullet()
                #add blullet to the list
                all_sprites_list.add(bullet) 
                bullet_list.add(bullet)
   
    # Call the update() method on all the sprites
    all_sprites_list.update()

    for bullet in bullet_list:
        enemy_hit_list=pygame.sprite.spritecollide(bullet, enemy_list,False)

        for enemy in enemy_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score+=1
            print(score)
        # remove thebullet if it flies up off the screen    
        if bullet.rect.y < wallTop:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


    screen.fill((200,200,200))
    #screen.blit(enemies.surf,enemies.rect)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


