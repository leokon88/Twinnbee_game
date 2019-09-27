import pygame

#initialize the game
windowHeight =600
windowWidth =400
margin =5 #offset from the edge
playerSpeed=1
bgSpeed=1
bulletSpeed=3

wallTop = margin
wallLeft = margin
wallRight =windowWidth - margin
wallBottom =windowHeight - margin

backgroundColor=(50,50,200) #initially set background color -blue

pygame.init()
clock=pygame.time.Clock() 

bullet_list=pygame.sprite.Group()
window = pygame.display.set_mode((windowWidth,windowHeight)) # tuple
pygame.display.set_caption('Twin Bee')

#load images
playerImg =pygame.image.load('images/twinbee.png')
backgroundImg=pygame.image.load('images/background.png')
bulletImg= pygame.image.load('images/bullet.png')

class Game:
    def __init__(self, bgImg, bgSpeed):
        self.backgroundImg=bgImg
        self.player=0
        self.bg1Location=0
        self.bg2Location=-bgImg.get_height() # above background1
        self.backgroundSpeed=bgSpeed
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

class Player:
    def __init__(self, img, speed):
        self.img = img
        self.xcoor= windowWidth/2 -img.get_width()/2  #centering the player
        self.ycoor= windowHeight *.80 # initially set player on 8/10 of the window at bottom
        self.isAlive=True
        self.speed = speed 
        self.ydir=0
        self.xdir=0

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

    # def shootBullet(self,img,bSpeed):
    #     self.bullet = Bullet(img,bSpeed)
    #     return self.bullet  

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
            #self.bulletImg=bImg
        self.speed=bulletSpeed
        self.image = pygame.Surface([4, 10])
        self.image.fill((10,12,14))
        self.rect =self.image.get_rect()
        # self.xloc=player.xcoor
        # self.yloc=player.ycoor*self.speed
       
 
     
   
    # def show(self):
    #     window.blit(self.bulletImg,self.bullet) #display image onto window
        
    def update(self):
        #self.yLoc += self.speed
        #self.bullet.insert(0,list(self.bullet))
      
        #self.show()
        self.rect.y -= 10
        #window.blit(self.rect) 

gameInstance=Game(backgroundImg,bgSpeed)
player=gameInstance.createPlayer(playerImg,playerSpeed)
#bullet =[player.shootBullet(bulletImg,bulletSpeed)]

#shoot=False
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
                bullet=Bullet()
                bullet.rect.x= player.xcoor
                bullet.rect.y = player.ycoor
                bullet_list.add(bullet)
        

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
    bullet_list.update()

    window.fill(backgroundColor)
    
    gameInstance.drawBackground()
    player.move()
    
    bullet_list.draw(window)

    #for loop through array.
    # for bullet in bullets:
    #     bullet.fired()
 
    pygame.display.flip()

    clock.tick(60)


 