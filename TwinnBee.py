import pygame
import random

windowHeight =400
windowWidth =400
margin =5 #offset from the edge
playerSpeed=1
bgSpeed=1
cloudSpeed=windowHeight/600
cloudAmount=2
bulletSpeed=5
bellSpeedInitial=1
gravity=0.03

shotDelayBar=20
shotDelayBarColor=(200,200,0) # yellow


wallTop = margin
wallLeft = margin
wallRight =windowWidth - margin
wallBottom =windowHeight - margin
shotDelayBarHeight= wallBottom

backgroundColor=(50,50,200) #initially set background color -blue

pygame.init()
clock=pygame.time.Clock() 

window = pygame.display.set_mode((windowWidth,windowHeight)) # tuple
pygame.display.set_caption('Twin Bee')

playerImg =pygame.image.load('images/twinbee.png')
backgroundImg=pygame.image.load('images/background.png')
bulletImage=pygame.image.load('images/bullet.png')
cloudImage=pygame.image.load('images/cloud.png')
bellImage=pygame.image.load('images/bell.png')

cloudOffset=cloudImage.get_width()/4
class Game:
    def __init__(self, bgImg, bgSpeed):
        self.backgroundImg=bgImg
        self.player=0
        self.bg1Location=0
        self.bg2Location=-bgImg.get_height() # above background1
        self.backgroundSpeed=bgSpeed
        self.bullets=[]
        self.clouds=[]
        self.bells=[]

    def createPlayer(self, img, pSpeed):
        self.player = Player(img,pSpeed)
        return self.player

    def drawBackground(self):
        self.bg1Location += self.backgroundSpeed
        self.bg2Location += self.backgroundSpeed
        if self.bg1Location == self.backgroundImg.get_height():
            self.bg1Location= -self.backgroundImg.get_height()
        if self.bg2Location == self.backgroundImg.get_height():
            self.bg2Location= -self.backgroundImg.get_height()
        window.blit(self.backgroundImg,(0,self.bg1Location))
        window.blit(self.backgroundImg,(0,self.bg2Location))
    
    def drawBullets(self):
        for bullet in self.bullets:
            bullet.move()
        if len(self.bullets)> 0:
            if self.bullets[len(self.bullets)-1].ycoor < 0:
                self.bullets.pop()
    
    def drawDelay(self,player):
        if player.delay>0:
            pygame.draw.rect(window,shotDelayBarColor,pygame.Rect(windowWidth/2- player.delay/2*windowWidth/50,
                shotDelayBarHeight,player.delay*windowWidth/50,2)) #surface to draw on,color, xcoor,ycoor, width,height
   
    def drawClouds(self):
        thisCloudSpeed=cloudSpeed
        if len(self.clouds)<cloudAmount: # create inital cloud 
            if len(self.clouds) >0:
                if self.clouds[0].speed == cloudSpeed:
                    thisCloudSpeed=cloudSpeed+ random.uniform(0,cloudSpeed)# initial speed 
            self.clouds.insert(0,Cloud(cloudImage, random.randint(wallLeft+windowWidth/8 -cloudImage.get_width(), wallRight-windowWidth/8),thisCloudSpeed))
        for cloud in self.clouds: # loop through clouds array
            cloud.move()
            if cloud.ycoor > wallBottom:
                cloud.ycoor = 0
                cloud.xcoor = random.randint(wallLeft+windowWidth/8 -cloudImage.get_width(), wallRight-windowWidth/8)
                cloud.speed = cloudSpeed + random.uniform(0,cloudSpeed)
                cloud.hasBell = True

    def drawBells(self):
        i=0
        bellRemove=-1
        for bell in self.bells:
            bell.move()
            if bell.ycoor > wallBottom:
                bellRemove=i
            i+=1
        if bellRemove >-1:
            self.bells.pop(bellRemove)


    def collision_bullet_cloud(self):
        for cloud in self.clouds:
            i=0
            bulletRemove = -1
            for bullet in self.bullets:
                if cloud.hasBell and\
                    bullet.ycoor<cloud.ycoor+cloud.height and\
                    bullet.ycoor>cloud.ycoor and\
                    bullet.xcoor+bullet.img.get_width()/2 > cloud.xcoor+cloudOffset and\
                    bullet.xcoor+bullet.img.get_width()/2 < cloud.xcoor+cloud.width-cloudOffset:
                    self.bells.insert(0,Bell(bellImage,cloud.xcoor+cloud.width/2-bellImage.get_width()/2,cloud.ycoor,bellSpeedInitial))
                    bulletRemove = i
                    cloud.hasBell=False
                i+=1
            if bulletRemove >-1:
                self.bullets.pop(bulletRemove)
    def collision_bullet_bell(self):
        for bell in self.bells:
            for bullet in self.bullets:
                if bullet.ycoor > bell.ycoor and bullet.ycoor < bell.ycoor + bell.height and\
                    bullet.xcoor >bell.xcoor and bullet.xcoor <bell.xcoor+bell.width:
                    bell.speed=bellSpeedInitial
                    bell.move()

class Player:
    def __init__(self, img, speed):
        self.img = img
        self.xcoor= windowWidth/2 -img.get_width()/2  #centering the player
        self.ycoor= windowHeight *.80 # initially set player on 8/10 of the window at bottom
        self.isAlive=True
        self.speed = speed 
        self.ydir=0
        self.xdir=0
        self.delay =0

    def show(self):
        window.blit(self.img,(self.xcoor,self.ycoor)) #display image onto window

    def move(self):
        newX = self.xcoor + self.xdir*self.speed
        if(newX>=wallLeft and newX <= wallRight-self.img.get_width()):
            self.xcoor =newX
        else:
            self.xcoor=self.xcoor

        newY = self.ycoor + self.ydir*self.speed 
        if(newY>=wallTop and newY <= wallBottom-self.img.get_height()):
            self.ycoor =newY
        else:
            self.ycoor=self.ycoor
        self.show()
    def shoot(self,game):
        bullet =Bullet(bulletImage, self.xcoor+self.img.get_width()/2 - bulletImage.get_width()/2, self.ycoor+3, bulletSpeed)
       
        if self.delay <=0:
            game.bullets.insert(0,bullet)
            self.delay= shotDelayBar

    def delayTick(self):
        if self.delay>0:
            self.delay-=1

class Bullet:
    def __init__(self,bulletImg,xcoor,ycoor,bulletSpeed):
        self.img=bulletImg
        self.xcoor=xcoor
        self.ycoor=ycoor
        self.speed=bulletSpeed

    def move(self):
        self.ycoor-=self.speed
        window.blit(self.img,((self.xcoor,self.ycoor)))

class Cloud:
    def __init__(self,cloudImage,xcoor,cloudSpeed):
        self.img=cloudImage
        self.xcoor=xcoor
        self.ycoor=0
        self.speed=cloudSpeed
        self.width = cloudImage.get_width()
        self.height = cloudImage.get_height()
        self.hasBell=True
    def move(self):
        self.ycoor +=self.speed
        window.blit(self.img,(self.xcoor,self.ycoor))

class Bell:
    def __init__(self,bellImage,xcoor,ycoor,bellSpeed):
        self.img=bellImage
        self.xcoor= xcoor
        self.ycoor= ycoor
        self.speed = bellSpeed
        self.initialSpeed=bellSpeed
        self.width = bellImage.get_width()
        self.height = bellImage.get_height()
    def move(self):
        self.ycoor -=self.speed
        self.speed -=gravity
        window.blit(self.img,(self.xcoor,self.ycoor))



gameInstance=Game(backgroundImg,bgSpeed)
player=gameInstance.createPlayer(playerImg,playerSpeed)
leftKeyPressed= False
rightKeyPressed =False
upKeyPressed= False
downKeyPressed =False

quitGame=False

while(True):
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key ==pygame.K_ESCAPE:
                quitGame=True
            elif event.key == pygame.K_LEFT:
                player.xdir = -1
                leftKeyPressed = True
            elif event.key  == pygame.K_RIGHT:
                player.xdir = 1
                RightKeyPressed = True
            elif event.key  == pygame.K_UP:
                player.ydir = -1
                upKeyPressed = True
            elif event.key  == pygame.K_DOWN:
                player.ydir = 1
                downKeyPressed = True
            elif event.key == pygame.K_SPACE:
                player.shoot(gameInstance)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                upKeyPressed= False
                if not downKeyPressed:
                    player.ydir= 0
            elif event.key == pygame.K_DOWN:
                downKeyPressed= False
                if not upKeyPressed:
                    player.ydir= 0
            elif event.key == pygame.K_LEFT:
                leftKeyPressed= False
                if not rightKeyPressed:
                    player.xdir= 0
            elif event.key == pygame.K_RIGHT:
                rightKeyPressed= False
                if not leftKeyPressed:
                    player.xdir= 0

    window.fill(backgroundColor)
    
    gameInstance.drawBackground()
    gameInstance.drawBullets()
    gameInstance.drawClouds()
    gameInstance.drawBells()
    gameInstance.collision_bullet_cloud()
    gameInstance.collision_bullet_bell()
    player.move()
    gameInstance.drawDelay(player)
    
    pygame.display.update()
    player.delayTick()
    clock.tick(60)


 